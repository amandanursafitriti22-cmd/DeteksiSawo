# Diagram Arsitektur Sistem SawoVision

## 1. Arsitektur Keseluruhan (System Architecture)

```mermaid
graph TB
    subgraph Client["🖥️ CLIENT LAYER (Browser)"]
        UI["React Frontend<br/>TanStack Router"]
        Webcam["Webcam Detector<br/>WebcamDetector.tsx"]
        Upload["Upload Detector<br/>UploadDetector.tsx"]
    end
    
    subgraph Model["🤖 MODEL INFERENCE LAYER"]
        ONNX["ONNX Runtime<br/>In-Browser Inference"]
        YOLOModel["YOLO v8/v11<br/>Detection Model"]
    end
    
    subgraph State["💾 STATE MANAGEMENT"]
        HistoryStore["History Store<br/>Detection Results"]
        SettingsStore["Settings Store<br/>User Preferences"]
    end
    
    subgraph Backend["☁️ BACKEND LAYER"]
        CloudflareWorkers["Cloudflare Workers<br/>Server.ts"]
        API["REST API<br/>Endpoints"]
    end
    
    subgraph Data["📦 DATA LAYER"]
        LocalStorage["Browser Storage<br/>localStorage"]
        Cache["Model Cache<br/>ONNX Files"]
    end
    
    subgraph Training["🎓 TRAINING LAYER"]
        TrainPipeline["Python Training<br/>YOLOv8/v11"]
        Dataset["Dataset Management<br/>Images & Labels"]
        ModelExport["Model Export<br/>PT → ONNX"]
    end
    
    UI -->|Input| Webcam
    UI -->|Input| Upload
    Webcam -->|Send Frame| ONNX
    Upload -->|Send Image| ONNX
    ONNX -->|Load Model| YOLOModel
    ONNX -->|Output| HistoryStore
    ONNX -->|Output| SettingsStore
    HistoryStore -->|Display| UI
    SettingsStore -->|Config| UI
    LocalStorage -->|Persist| HistoryStore
    LocalStorage -->|Persist| SettingsStore
    Cache -->|Load| YOLOModel
    CloudflareWorkers -->|Serve| API
    TrainPipeline -->|Generate| ModelExport
    ModelExport -->|Deploy| Cache
    Dataset -->|Train| TrainPipeline
```

---

## 2. Frontend Architecture (Presentasi Layer)

```mermaid
graph LR
    subgraph Routes["📄 ROUTES"]
        Home["index.tsx<br/>Home Page"]
        Detect["detect.tsx<br/>Detection"]
        Upload["upload.tsx<br/>Upload Page"]
        History["history.tsx<br/>History Page"]
        Info["info.tsx<br/>Info Page"]
        Settings["settings.tsx<br/>Settings"]
        Dashboard["dashboard.tsx<br/>Dashboard"]
    end
    
    subgraph Components["🧩 COMPONENTS"]
        Layout["Layout Components"]
        Detection["Detection Components"]
        UI["UI Components<br/>Radix UI + Tailwind"]
    end
    
    subgraph Hooks["🎣 HOOKS"]
        UseMobile["use-mobile<br/>Responsive"]
    end
    
    subgraph Lib["📚 UTILITIES"]
        Utils["utils.ts"]
        Theme["theme.tsx"]
        Export["export.ts"]
        ErrorCapture["error-capture.ts"]
        YOLO["yolo/"]
    end
    
    Routes -->|Render| Components
    Components -->|Use| Hooks
    Components -->|Use| Lib
    Components -->|UI| UI
```

---

## 3. Detection Pipeline (Real-time Flow)

```mermaid
graph TD
    Input["📹 Input<br/>Webcam or File"]
    Preprocess["🔄 Preprocessing<br/>Normalize, Resize"]
    Inference["🤖 YOLO Inference<br/>ONNX Runtime"]
    PostProcess["✨ Post-processing<br/>NMS, Filtering"]
    Results["📊 Results<br/>Detections"]
    Visualization["🎨 Visualization<br/>Draw Bboxes"]
    Store["💾 Store Results<br/>History Store"]
    Display["📺 Display<br/>UI Update"]
    
    Input -->|Frame| Preprocess
    Preprocess -->|Tensor| Inference
    Inference -->|Raw Output| PostProcess
    PostProcess -->|Filtered| Results
    Results -->|Coordinates| Visualization
    Results -->|Save| Store
    Visualization -->|Canvas| Display
    Store -->|Retrieve| Display
```

---

## 4. State Management Architecture

```mermaid
graph LR
    subgraph Store["🏪 STORES"]
        History["historyStore.ts<br/>Detection History"]
        Settings["settingsStore.ts<br/>User Settings"]
    end
    
    subgraph Actions["⚡ ACTIONS"]
        AddDetection["Add Detection"]
        ClearHistory["Clear History"]
        SaveSettings["Save Settings"]
        LoadSettings["Load Settings"]
    end
    
    subgraph Persistence["💾 PERSISTENCE"]
        LocalStorage["localStorage"]
        SessionStorage["sessionStorage"]
    end
    
    Store -->|Execute| Actions
    Actions -->|Write| Persistence
    Persistence -->|Read| Store
    Persistence -->|Subscribe| Store
```

---

## 5. Model Training Pipeline

```mermaid
graph TD
    subgraph Data["📁 DATA PREPARATION"]
        Raw["Raw Images"]
        LabelStudio["Label Studio<br/>Annotation"]
        Convert["convert_label_studio.py<br/>Convert Labels"]
    end
    
    subgraph Processing["🔧 PREPROCESSING"]
        Setup["setup_dataset.py<br/>Dataset Setup"]
        Split["fix_split.py<br/>Train/Val Split"]
        Augment["Data Augmentation"]
    end
    
    subgraph Training["🎓 MODEL TRAINING"]
        TrainLocal["train_local.py<br/>Local Training"]
        TrainColab["train_colab.ipynb<br/>GPU Training"]
        YOLOv8["YOLOv8/v11<br/>Training"]
    end
    
    subgraph Export["📦 MODEL EXPORT"]
        BestModel["best.pt<br/>PyTorch Model"]
        ConvertONNX["Convert to ONNX"]
        FinalModel["best.onnx<br/>Deployed Model"]
    end
    
    subgraph Validation["✅ VALIDATION"]
        TestDetection["test_detection.py"]
        TestModel["test_model.py"]
        Benchmark["inference_benchmark.py"]
    end
    
    Raw -->|Annotate| LabelStudio
    LabelStudio -->|Convert| Convert
    Convert -->|Prepare| Setup
    Setup -->|Split| Split
    Split -->|Augment| Augment
    Augment -->|Train| TrainLocal
    Augment -->|Train| TrainColab
    TrainLocal -->|Output| YOLOv8
    TrainColab -->|Output| YOLOv8
    YOLOv8 -->|Save| BestModel
    BestModel -->|Convert| ConvertONNX
    ConvertONNX -->|Output| FinalModel
    FinalModel -->|Deploy| Validation
    Validation -->|Metrics| Benchmark
```

---

## 6. File Structure & Components

```mermaid
graph TB
    subgraph SrcTree["📂 SRC/"]
        Routes["routes/"]
        Components["components/"]
        Hooks["hooks/"]
        Lib["lib/"]
        Stores["stores/"]
    end
    
    subgraph CompTree["components/"]
        Detection["detection/<br/>UploadDetector<br/>WebcamDetector"]
        Layout["layout/<br/>Navbar, Footer<br/>ThemeToggle"]
        UI["ui/<br/>Radix Components"]
    end
    
    subgraph LibTree["lib/"]
        Utils["utils.ts"]
        Theme["theme.tsx"]
        YOLO["yolo/"]
        Error["error-capture.ts"]
    end
    
    SrcTree --> Routes
    SrcTree --> Components
    SrcTree --> Hooks
    SrcTree --> Lib
    SrcTree --> Stores
    Components --> Detection
    Components --> Layout
    Components --> UI
    Lib --> Utils
    Lib --> Theme
    Lib --> YOLO
    Lib --> Error
```

---

## 7. Data Flow: Deteksi Real-time

```mermaid
sequenceDiagram
    actor User
    participant UI as React UI
    participant Detector as Detector<br/>Component
    participant ONNX as ONNX Runtime
    participant Store as History Store
    participant Canvas as Canvas/Display
    
    User->>UI: Click Start Webcam
    UI->>Detector: Initialize Webcam
    Detector->>Detector: Request Permissions
    
    loop Real-time Detection
        Detector->>Detector: Capture Frame
        Detector->>ONNX: Send Frame Data
        ONNX->>ONNX: Preprocess
        ONNX->>ONNX: Run Inference
        ONNX->>ONNX: Post-process
        ONNX->>Detector: Return Detections
        Detector->>Store: Save to History
        Detector->>Canvas: Draw Results
        Canvas->>UI: Update Display
    end
    
    User->>Detector: Stop Detection
    Detector->>UI: Cleanup Resources
```

---

## 8. Technology Stack

```mermaid
graph TB
    subgraph Frontend["FRONTEND"]
        React["React 18+"]
        Router["TanStack Router"]
        Query["TanStack Query"]
        UI["Radix UI"]
        Styling["Tailwind CSS"]
    end
    
    subgraph Inference["INFERENCE"]
        ONNX["ONNX Runtime<br/>In-Browser"]
        YOLO["YOLO v8/v11<br/>Model"]
    end
    
    subgraph Backend["BACKEND"]
        Vite["Vite"]
        CF["Cloudflare Workers"]
    end
    
    subgraph Training["TRAINING"]
        Python["Python 3.8+"]
        YOLOTrain["Ultralytics YOLOv8"]
        Torch["PyTorch"]
        LabelStudio["Label Studio"]
    end
    
    subgraph Build["BUILD & DEPLOY"]
        Vite -->|Build| Frontend
        Frontend -->|Deploy| CF
    end
    
    Python -->|Train| YOLOTrain
    YOLOTrain -->|Use| Torch
    Torch -->|Export| ONNX
    Inference -->|Load| YOLO
```

---

## 9. Deployment Architecture

```mermaid
graph LR
    Dev["👨‍💻 Development<br/>Local Machine"]
    Build["🔨 Build Process<br/>Vite Build"]
    Dist["📦 Distribution<br/>dist/ folder"]
    CDN["🌐 CDN<br/>Static Assets"]
    CF["☁️ Cloudflare Workers<br/>Server.ts"]
    Browser["🖥️ Browser<br/>User Client"]
    
    Dev -->|npm run build| Build
    Build -->|Output| Dist
    Dist -->|Publish| CDN
    Dist -->|Deploy| CF
    CDN -->|Serve| Browser
    CF -->|API| Browser
    Browser -->|Load Models| CDN
```

---

## 10. Key Features Architecture

```mermaid
graph TB
    subgraph Features["🎯 CORE FEATURES"]
        WebcamDetection["📹 Webcam Detection<br/>Real-time Analysis"]
        UploadDetection["📤 Upload Detection<br/>Image Analysis"]
        HistoryTracking["📊 History Tracking<br/>Detection Results"]
        SettingsConfig["⚙️ Settings Config<br/>User Preferences"]
        ThemeSwitcher["🎨 Theme Switcher<br/>Light/Dark Mode"]
    end
    
    subgraph Support["🛠️ SUPPORT FEATURES"]
        ErrorHandling["❌ Error Handling"]
        ResponseDesign["📱 Responsive Design"]
        Performance["⚡ Performance"]
        Documentation["📚 Documentation"]
    end
    
    Features --> Support
```

---

## Catatan Arsitektur:

1. **Frontend-First Architecture**: Model inference berjalan di browser (ONNX Runtime) untuk latency rendah
2. **Server-Side Rendering**: Menggunakan TanStack Start untuk SSR capabilities
3. **State Management**: Zustand untuk history dan settings store
4. **Model Format**: PyTorch untuk training, ONNX untuk deployment
5. **Responsive Design**: Mobile-first dengan Tailwind CSS + Radix UI
6. **Training Pipeline**: Python-based untuk model development
7. **Scalable**: Cloudflare Workers untuk backend scalability
