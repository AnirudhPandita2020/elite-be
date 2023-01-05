from enum import Enum


class CertificateEnum(Enum):
    road_tax = "Road Tax"
    fitness_certificate = "Fitness Certificate"
    goods_certificate_permission = "Goods Carrier Permission"
    permit = "Permit"
    green_tax = "Green Tax"
    insurance = "Insurance"
    pollution = "Pollution"


class Sites(Enum):
    KPCL = "KPCL"
    KKD = "KKD"
    KAT = "KAT"
    VIZ = "VIZ"
    SHE = "SHE"
