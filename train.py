from ultralytics import YOLO
import multiprocessing

# yaml会自动下载
def main():
    model = YOLO("yolo11s-rtdetr.yaml")
        # Train the model
    results = model.train(data="vindr.yaml", batch=16,epochs=300, imgsz=640)

if __name__=='__main__':
    multiprocessing.freeze_support()
    main()