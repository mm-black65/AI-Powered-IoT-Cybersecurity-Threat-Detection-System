from pydantic import BaseModel, Field

class ThreatFeatures(BaseModel):
    flow_duration: float
    Header_Length: float

    Protocol_Type: float = Field(alias="Protocol Type")

    Duration: float
    Rate: float
    Srate: float

    fin_flag_number: float
    syn_flag_number: float
    rst_flag_number: float
    psh_flag_number: float
    ack_flag_number: float

    ack_count: float
    syn_count: float
    fin_count: float
    urg_count: float
    rst_count: float

    HTTP: float
    HTTPS: float
    DNS: float
    TCP: float
    UDP: float
    ARP: float
    ICMP: float
    IPv: float
    LLC: float

    Tot_sum: float = Field(alias="Tot sum")

    Min: float
    Max: float
    AVG: float
    Std: float

    Tot_size: float = Field(alias="Tot size")

    IAT: float
    Number: float
    Magnitue: float
    Radius: float
    Covariance: float
    Variance: float
    Weight: float

    model_config = {
        "populate_by_name": True
    }