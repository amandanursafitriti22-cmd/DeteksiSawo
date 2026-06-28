# Place your YOLOv11 ONNX model here

The app loads the model from `/models/best.onnx` (this folder, served by Vite).

## Export from your trained `best.pt`

```bash
pip install ultralytics
yolo export model=best.pt format=onnx opset=12 imgsz=640 dynamic=False simplify=True
```

Then copy the resulting file:

```
mv best.onnx public/models/best.onnx
```

Reload the app — the badge in `/detect` will switch from "Mode Demo" to
"Model: best.onnx".

## Class order

The model must output 3 classes in this exact order:

1. `belum_matang`
2. `setengah_matang`
3. `matang`

If your training used a different order, edit `src/lib/yolo/types.ts`
(`CLASS_NAMES`) accordingly.
