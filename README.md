# RISC-V PPA Study Architecture

## Directory Structure

```
riscv-ppa-study/
├── WORKSPACE.bazel                 # Bazel workspace configuration
├── MODULE.bazel                    # Bazel module dependencies
├── BUILD.bazel                     # Root build file
├── .bazelrc                        # Bazel configuration
├── README.md                       # Project documentation
│
├── design/                         # Design artifacts (what we're studying)
│   ├── software/                   # Software applications and benchmarks
│   │   ├── common/                 # Shared utilities and profiling
│   │   ├── fft/                    # FFT benchmark variants
│   │   ├── matrix_mult/            # Matrix multiplication workloads
│   │   └── crypto/                 # Cryptographic workloads
│   │
│   └── hardware/                   # Hardware design and implementation
│       ├── rtl/                    # RTL design and simulation
│       │   ├── cores/              # RISC-V core designs (Rocket, VexRiscv, CVA6)
│       │   ├── testbench/          # Universal parameterized testbench
│       │   ├── simulation/         # RTL simulation infrastructure
│       │   └── common/             # Shared RTL components
│       │
│       └── physical/               # Physical implementation (PDK-dependent)
│           ├── sky130/             # SkyWater 130nm implementation
│           ├── generic/            # Generic/educational PDK
│           ├── future_nodes/       # Advanced technology nodes
│           └── common/             # PDK-independent utilities
│
├── flows/                          # Process definitions (how designs flow through infrastructure)
│   ├── main_study_flow.py          # Complete PPA study orchestration
│   ├── software_flow.py            # Software compilation and execution
│   ├── simulation_flow.py          # RTL simulation workflows
│   ├── synthesis_flow.py           # Physical implementation workflows
│   ├── analysis_flow.py            # Results analysis workflows
│   │
│   ├── tasks/                      # Individual process steps
│   ├── bazel/                      # Build process definitions
│   └── utils/                      # Flow utilities and common steps
│
├── infrastructure/                 # Infrastructure & environment (where we execute)
│   ├── nix/                        # Reproducible tool environments
│   ├── kubernetes/                 # Distributed compute orchestration
│   ├── terraform/                  # Infrastructure provisioning
│   ├── cloud-research/             # Research area for deployment tools
│   └── targets/                    # Hardware execution environments
│
├── analysis/                       # Results processing and outputs
│   ├── scripts/                    # Analysis and visualization tools
│   ├── data/                       # Raw measurement data (flow outputs)
│   └── targets/                    # Final study deliverables
│
├── docs/                           # Documentation
├── third_party/                    # External dependencies
└── configs/                        # Environment configurations
```

## Conceptual Model: Design → Flows → Infrastructure → Targets

```mermaid
graph LR
    subgraph "📋 Design (What we study)"
        D1[Software Applications<br/>FFT, Matrix, Crypto]
        D2[Hardware Cores<br/>Rocket, VexRiscv, CVA6]
        D3[Technology Nodes<br/>Sky130, Generic, Future]
    end
    
    subgraph "🔄 Flows (How we study)"
        F1[Compilation Flow<br/>Rust → RISC-V binaries]
        F2[Simulation Flow<br/>RTL + software → traces]
        F3[Synthesis Flow<br/>RTL + PDK → silicon]
        F4[Analysis Flow<br/>Results → insights]
    end
    
    subgraph "🏭 Infrastructure (Where we study)"
        I1[Nix Environment<br/>Reproducible tools]
        I2[Kubernetes Cluster<br/>Distributed compute]
        I3[Bazel Cache<br/>Build artifacts]
        I4[Prefect Workers<br/>Task execution]
    end
    
    subgraph "🎯 Targets (What we produce)"
        T1[3D PPA Visualizations<br/>Performance comparisons]
        T2[Design Recommendations<br/>Optimal configurations]
        T3[Scaling Studies<br/>Technology insights]
    end
    
    D1 -->|flows through| F1
    D2 -->|flows through| F2
    D3 -->|flows through| F3
    
    F1 -->|executes on| I1
    F2 -->|executes on| I2
    F3 -->|executes on| I3
    F4 -->|executes on| I4
    
    I1 -->|produces| T1
    I2 -->|produces| T2
    I3 -->|produces| T3
    
    style D1 fill:#e3f2fd
    style F1 fill:#f3e5f5
    style I1 fill:#e8f5e8
    style T1 fill:#fff8e1
```

## Tool Philosophy: Composition of Simple, Well-Defined Tools

```mermaid
graph LR
    subgraph "Unix Philosophy Applied"
        A["🔧 Nix<br/>Dependencies &<br/>Reproducible Envs"]
        B["🏗️ Bazel<br/>Builds &<br/>Intelligent Caching"]  
        C["🔄 Prefect<br/>Workflow<br/>Orchestration"]
        D["☸️ Kubernetes<br/>Distributed<br/>Computing"]
    end
    
    subgraph "Clean Interfaces"
        A -->|provides env| B
        B -->|builds artifacts| C  
        C -->|launches tasks| D
        D -->|schedules on| E["💻 Compute Resources"]
    end
    
    subgraph "Single Responsibilities"
        A1["✅ Nix: Do ONE thing well<br/>• Reproducible environments<br/>• Dependency management<br/>• Version pinning"]
        
        B1["✅ Bazel: Do ONE thing well<br/>• Build orchestration<br/>• Incremental compilation<br/>• Artifact caching"]
        
        C1["✅ Prefect: Do ONE thing well<br/>• Workflow dependencies<br/>• Resource allocation<br/>• Monitoring & retries"]
        
        D1["✅ Kubernetes: Do ONE thing well<br/>• Container scheduling<br/>• Resource management<br/>• Service discovery"]
    end
    
    subgraph "Composability Benefits"
        F1["🔄 Easy to Replace<br/>• Swap Bazel → Buck2<br/>• Swap K8s → Nomad<br/>• Swap Prefect → Airflow"]
        
        F2["🐛 Easy to Debug<br/>• Each layer isolated<br/>• Clear responsibility<br/>• Simple interfaces"]
        
        F3["📈 Easy to Scale<br/>• Add tools independently<br/>• No vendor lock-in<br/>• Incremental adoption"]
    end
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5  
    style C fill:#e8f5e8
    style D fill:#fff8e1
    style A1 fill:#e3f2fd
    style B1 fill:#f3e5f5
    style C1 fill:#e8f5e8 
    style D1 fill:#fff8e1
```

## Prefect Pipeline Flow

```mermaid
graph TD
    A[Start PPA Study] --> B[Configure Study Parameters]
    B --> C[Compile Software Applications]
    
    C --> D1[Compile for Rocket + Baseline ISA]
    C --> D2[Compile for Rocket + Vector ISA] 
    C --> D3[Compile for VexRiscv + Baseline ISA]
    C --> D4[Compile for VexRiscv + Compressed ISA]
    C --> D5[Compile for CVA6 + All Extensions]
    
    D1 --> E1[Simulate on Rocket Core]
    D2 --> E1
    D3 --> E2[Simulate on VexRiscv Core]
    D4 --> E2
    D5 --> E3[Simulate on CVA6 Core]
    
    E1 --> F1[Generate Switching Activity - Rocket]
    E2 --> F2[Generate Switching Activity - VexRiscv]  
    E3 --> F3[Generate Switching Activity - CVA6]
    
    F1 --> G1[Synthesize Rocket + Sky130]
    F1 --> G2[Synthesize Rocket + Generic PDK]
    F2 --> G3[Synthesize VexRiscv + Sky130]
    F2 --> G4[Synthesize VexRiscv + Generic PDK]
    F3 --> G5[Synthesize CVA6 + Sky130]
    F3 --> G6[Synthesize CVA6 + Generic PDK]
    
    G1 --> H1[Place & Route - R+Sky130]
    G2 --> H2[Place & Route - R+Generic]
    G3 --> H3[Place & Route - V+Sky130]
    G4 --> H4[Place & Route - V+Generic]
    G5 --> H5[Place & Route - C+Sky130]
    G6 --> H6[Place & Route - C+Generic]
    
    H1 --> I[Power Analysis]
    H2 --> I
    H3 --> I
    H4 --> I
    H5 --> I
    H6 --> I
    
    E1 --> J[Performance Analysis]
    E2 --> J
    E3 --> J
    
    H1 --> K[Area Analysis]
    H2 --> K
    H3 --> K
    H4 --> K
    H5 --> K
    H6 --> K
    
    I --> L[Generate PPA Report]
    J --> L
    K --> L
    
    L --> M[3D Visualization & Analysis]
    M --> N[Design Space Recommendations]
    
    style A fill:#e1f5fe
    style L fill:#f3e5f5
    style M fill:#e8f5e8
    style N fill:#fff3e0
```

## Architecture Stack

```mermaid
graph TB
    subgraph "Analysis Layer"
        A1[3D PPA Visualization]
        A2[Design Space Analysis] 
        A3[Pareto Frontier Analysis]
        A4[Technology Scaling Studies]
    end
    
    subgraph "Orchestration Layer - Prefect"
        O1[Study Flow Controller]
        O2[Resource Management]
        O3[Task Dependencies]
        O4[Failure Handling & Retries]
        O5[Progress Monitoring]
    end
    
    subgraph "Build & Compilation Layer - Bazel"
        B1[Rust Software Builds]
        B2[Multi-target Compilation] 
        B3[ISA Extension Variants]
        B4[Dependency Management]
    end
    
    subgraph "Verification Layer"
        V1[Universal Testbench]
        V2[Core Interface Wrappers]
        V3[Stimulus Generation]
        V4[Performance Monitors]
        V5[Correctness Checkers]
    end
    
    subgraph "Hardware Design Layer" 
        HD1[Hardware Design - RTL Cores]
        HD2[Universal Testbench]
        HD3[Interface Wrappers]
        HD4[Simulation Models]
    end
    
    subgraph "Physical Implementation Layer"
        PI1[Synthesis (RTL → Gates)]
        PI2[Place & Route]  
        PI3[Technology Mapping]
        PI4[Power/Timing Analysis]
    end
    
    subgraph "Technology Layer"
        T1[Sky130 PDK]
        T2[Generic PDK] 
        T3[Future Technology Nodes]
    end
    
    subgraph "Infrastructure Layer"
        I1[RISC-V Hardware Boards]
        I2[High-Memory Synthesis Servers]
        I3[GPU Simulation Accelerators]
        I4[Cloud Compute Resources]
    end
    
    A1 -.->|analyze| O1
    O1 -->|orchestrate| B1
    B1 -->|compile| V1
    V1 -->|verify| HD1
    HD1 -->|implement| PI1
    PI1 -->|layout| T1
    PI1 -->|layout| T2
    O2 -->|manage| I1
    O2 -->|manage| I2
    
    style A1 fill:#e3f2fd
    style O1 fill:#f3e5f5  
    style V1 fill:#e8f5e8
    style PI1 fill:#fff8e1
    style T1 fill:#fce4ec
```

## Core Design Principles

### Mental Model
**Design Artifacts** (the subject matter) → **Process Flows** (the methodology) → **Infrastructure** (the execution environment) → **Target Results** (the deliverables)

### Tool Responsibilities
- **Nix**: Reproducible environments and dependency management
- **Bazel**: Build orchestration and intelligent caching  
- **Prefect**: Workflow execution and pipeline orchestration
- **Kubernetes**: Scalable distributed computing

### Key Architectural Benefits
- **Clean separation**: Design (what) vs Flows (how) vs Infrastructure (where) vs Targets (results)
- **Universal testbench**: Single verification environment for fair core comparison
- **PDK-separated physical implementation**: Technology-specific synthesis flows
- **Composable tools**: Each tool excels in its domain with clean interfaces
- **3D analysis space**: Core design × PDK technology × software workloads

### Implementation Philosophy
Following Unix philosophy: compose simple tools that do one thing exceptionally well, rather than building monolithic solutions. This trades implementation complexity (building custom tools) for operational complexity (managing multiple specialized tools).