    +----------------------+
    |  Data Preprocessing  |
    +----------------------+
              |
              v
    +-------------------+
    | Load Dataset      |
    | Drop Missing      |
    | Split Features    |
    | Generate Labels   |
    +-------------------+
              |
              v
    +-----------------+      +-------------------+
    | Model Training  | ---> |  Model Training   |
    +-----------------+      |                   |
              |              |                   |
              v              v                   |
    +-----------------+      +-------------------+
    | Random Forest   |      |Logistic Regression|
    | Classifier      |      |                   |
    +-----------------+      +-------------------+
              |              |                   |
              v              v                   |
    +-----------------+      +-------------------+
    | Model Evaluation|      | Model Evaluation  |
    +-----------------+      +-------------------+
              |              |                   |
              v              v                   |
    +-----------------+      +-------------------+
    | Backtesting     |      | Backtesting       |
    +-----------------+      +-------------------+
              |              |                   |
              v              v                   |
    +-----------------+      +-------------------+
    | Calculate Stock |      | Calculate Stock   |
    | and Market      |      | and Market        |
    | Returns         |      | Returns           |
    +-----------------+      +-------------------+
              |              |                   |
              v              v                   |
    +-----------------+      +-------------------+
    | Compare         |      | Compare           |
    | Performance     |      | Performance       |
    +-----------------+      +-------------------+
