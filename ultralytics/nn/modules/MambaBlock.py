import torch
import torch.nn as nn
import torch.nn.functional as F

from mamba_ssm import Mamba

class MambaLayer(nn.Module):
    def __init__(self, dim, d_state = 16, d_conv = 4, expand = 2):
        super().__init__()
        self.dim = dim
        self.norm = nn.LayerNorm(dim)
        self.mamba = Mamba(
                d_model=dim, # Model dimension d_model
                d_state=d_state,  # SSM state expansion factor
                d_conv=d_conv,    # Local convolution width
                expand=expand,    # Block expansion factor
                bimamba_type="v2",
        )
        self.conv = nn.Conv2d(dim, dim, 3, 1, 1)
    
    def forward(self, x):
        device = "CUDA" if x.is_cuda else "CPU"
        if device=="CPU":
            x = self.conv(x)
            return x
        elif device=="CUDA": 
            B, C = x.shape[:2]
            assert C == self.dim
            n_tokens = x.shape[2:].numel()
            img_dims = x.shape[2:]
            x_flat = x.reshape(B, C, n_tokens).transpose(-1, -2)
            x_norm = self.norm(x_flat)
            x_mamba = self.mamba(x_norm)
            out = x_mamba.transpose(-1, -2).reshape(B, C, *img_dims)
            return out
    
class mamba_block(nn.Module):
    def __init__(self, c1, c2, shortcut=True, expand=2):
        
        super().__init__()
        assert c1 == c2
        expand = int(expand * c1)
        self.mamba = MambaLayer(dim=c1, d_state = 16, d_conv = 4, expand = 2)
        self.norm = nn.BatchNorm2d(c1)
        self.conv1 = nn.Conv2d(c1, expand, 1)
        self.relu = nn.GELU()
        self.conv2 = nn.Conv2d(expand, c2, 1)
        

    def forward(self, x):
        # res = x
        x = self.mamba(x) + x
        res = self.norm(x)
        x = self.conv1(res)
        x = self.relu(x)
        x = self.conv2(x) + res
        
        return x
    
    
    
    
import torch.nn.functional as F
    
class Gated_Fusion(nn.Module):
    def __init__(self, c1=[256, 128, 64], c2=256, n=1, shortcut=True, g=1, e=0.5):
        super().__init__()
        
        self.conv_x = nn.Conv2d(c1[0], c1[0], 1, 1, bias=False)
        self.conv_y = nn.Conv2d(c1[1], c1[0], 1, 1, bias=False)
        self.conv_z = nn.Conv2d(c1[2], c1[0], 1, 1, bias=False)
        
        self.DWConv = nn.Sequential(
            nn.Conv2d(c1[0], c1[0], 3, 1, 1, groups=c1[0]),
        )
        self.bn = nn.LayerNorm(c2)
        self.act = nn.GELU()
        
        self.conv_linear1 = Conv(c1[0], c1[0], 1, 1)
        self.conv_linear2 = Conv(c1[0], c1[0], 1, 1)
        
        # self.mamba = MambaLayer(dim=c1[0], d_state = 16, d_conv = 4, expand = 2)
        
    def forward(self, inputs):
        x = inputs[0]
        y = inputs[1]
        z = inputs[2]
        
        res_x = x
        
        x_k = self.conv_x(x)
        
        input_size = x.size()
        
        y_q = self.conv_y(y)
        y_q = F.interpolate(y_q, size=[input_size[2], input_size[3]],
                            mode="bilinear", align_corners=False)
        
        z_q = self.conv_z(z)
        z_q = F.interpolate(z_q, size=[input_size[2], input_size[3]],
                            mode="bilinear", align_corners=False)
        
        sim_map_xy = torch.sigmoid(torch.sum(x_k * y_q, dim=1).unsqueeze(1))
        sim_map_xz = torch.sigmoid(torch.sum(x_k * z_q, dim=1).unsqueeze(1))
        
        xy = (1-sim_map_xy)*x + sim_map_xy*y_q
        xz = (1-sim_map_xz)*x + sim_map_xz*z_q
        
        fusion = self.conv_linear1(xy + xz)
        
        fusion += res_x
        
        fusion = self.conv_linear2(fusion)
        
        return fusion
    
    
class downsample(nn.Module):
    def __init__(self, c1, c2, k=1, s=1, p=None, g=1, d=1, act=True):
        super().__init__()
        self.bn = nn.BatchNorm2d(c1)
        
        self.dwconv = nn.Conv2d(c1, c1, 3, 2, 1, groups=c1, dilation=d, bias=False)
        
        self.conv1x1 = nn.Conv2d(c1, c2, 1, 1, 0, groups=1, dilation=d, bias=False)
        
        self.linear1 = nn.Conv2d(c2, c2*2, 1, 1, 0, groups=1, dilation=d, bias=False)
        self.act = nn.SiLU()
        self.linear2 = nn.Conv2d(c2*2, c2, 1, 1, 0, groups=1, dilation=d, bias=False)
        
        
    def forward(self, x):
        x = self.dwconv(x)
        x = self.bn(x)
        x = self.conv1x1(x)
        res = x
        x = self.linear1(x)
        x = self.act(x)
        x = self.linear2(x)
        
        return x + res
    
    def forward_fuse(self, x):
        x = self.dwconv(x)
        x = self.conv1x1(x)
        res = x
        x = self.linear1(x)
        x = self.act(x)
        x = self.linear2(x)
        
        return x + res