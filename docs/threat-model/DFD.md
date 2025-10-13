# DFD — Data Flow Diagram

```mermaid
graph TD
    %% Trust Boundaries
    subgraph Client [Trust Boundary: Client]
        U[User]
    end

    subgraph Edge [Trust Boundary: Edge/API]
        A[API Gateway]
    end

    subgraph Core [Trust Boundary: Core Service]
        S[MediaService]
        DB[(Database)]
    end

    U -->|F1: Auth request| A
    A -->|F2: JWT token| U
    A -->|F3: Media upload| S
    S -->|F4: Store metadata| DB
    DB -->|F5: Read media info| S
