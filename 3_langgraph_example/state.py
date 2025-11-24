# state.py
from typing import Optional, List, Dict, Any
from ibm_watsonx_gov.entities.state import EvaluationState


class AppState(EvaluationState):
    """
    State che estende EvaluationState per supportare le metriche IBM Watsonx Gov.
    EvaluationState già include i campi necessari per le metriche:
    - input_text
    - context
    - generated_text
    - tool_name (potrebbe essere necessario aggiungerlo)
    """
    # Campi aggiuntivi per il tuo applicativo
    domain: str = ""
    student_id: str = ""
    message_id: Optional[str] = None
    
    # Campi per i tool
    tool_name: Optional[str] = None
    tool_args: Optional[Dict[str, Any]] = None
    tool_output: Optional[Any] = None