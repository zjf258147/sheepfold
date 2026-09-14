from datetime import datetime

from sqlalchemy.orm import Session

from app.models.sequence import SequenceCounter


def _next_seq(db: Session, seq_type: str) -> int:
    """获取并递增当日序列号（事务内调用）。"""
    today = datetime.now().strftime("%Y%m%d")
    counter = (
        db.query(SequenceCounter)
        .filter(SequenceCounter.seq_type == seq_type, SequenceCounter.seq_date == today)
        .with_for_update()
        .first()
    )
    if counter is None:
        counter = SequenceCounter(seq_type=seq_type, seq_date=today, current_value=0)
        db.add(counter)
        db.flush()
    counter.current_value += 1
    db.flush()
    return counter.current_value


def generate_inbound_no(db: Session) -> str:
    """生成入库单号：JIN-{YYYYMMDD}-{序号4位}。"""
    seq = _next_seq(db, "JIN")
    today = datetime.now().strftime("%Y%m%d")
    return f"JIN-{today}-{seq:04d}"


def generate_outbound_no(db: Session) -> str:
    """生成出库单号：JOUT-{YYYYMMDD}-{序号4位}。"""
    seq = _next_seq(db, "JOUT")
    today = datetime.now().strftime("%Y%m%d")
    return f"JOUT-{today}-{seq:04d}"


def generate_rc_no(db: Session) -> str:
    """生成到货单号：RC{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "RC")
    today = datetime.now().strftime("%Y%m%d")
    return f"RC{today}{seq:03d}"


def generate_inspection_no(db: Session) -> str:
    """生成检验编号：JC{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "JC")
    today = datetime.now().strftime("%Y%m%d")
    return f"JC{today}{seq:03d}"


def generate_return_no(db: Session) -> str:
    """生成退货单号：TH{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "TH")
    today = datetime.now().strftime("%Y%m%d")
    return f"TH{today}{seq:03d}"


def generate_fc_no(db: Session) -> str:
    """生成返厂单号：FC{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "FC")
    today = datetime.now().strftime("%Y%m%d")
    return f"FC{today}{seq:03d}"


def generate_diag_no(db: Session) -> str:
    """生成诊断编号：DG{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "DG")
    today = datetime.now().strftime("%Y%m%d")
    return f"DG{today}{seq:03d}"


def generate_repair_no(db: Session) -> str:
    """生成维修工单号：WX{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "WX")
    today = datetime.now().strftime("%Y%m%d")
    return f"WX{today}{seq:03d}"


def generate_scrap_no(db: Session) -> str:
    """生成报废单号：BF{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "BF")
    today = datetime.now().strftime("%Y%m%d")
    return f"BF{today}{seq:03d}"


def generate_reship_no(db: Session) -> str:
    """生成再出货单号：RH{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "RH")
    today = datetime.now().strftime("%Y%m%d")
    return f"RH{today}{seq:03d}"


def generate_stocktake_no(db: Session) -> str:
    """生成盘点单号：PD{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "PD")
    today = datetime.now().strftime("%Y%m%d")
    return f"PD{today}{seq:03d}"


def generate_adjustment_no(db: Session) -> str:
    """生成调整单号：TZ{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "TZ")
    today = datetime.now().strftime("%Y%m%d")
    return f"TZ{today}{seq:03d}"


def generate_shipment_no(db: Session) -> str:
    """生成出货单号：SH{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "SH")
    today = datetime.now().strftime("%Y%m%d")
    return f"SH{today}{seq:03d}"


def generate_bom_no(db: Session) -> str:
    """生成BOM编号：BOM{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "BOM")
    today = datetime.now().strftime("%Y%m%d")
    return f"BOM{today}{seq:03d}"


def generate_task_no(db: Session) -> str:
    """生成生产任务编号：PR{YYYYMMDD}{序号3位}。"""
    seq = _next_seq(db, "PR")
    today = datetime.now().strftime("%Y%m%d")
    return f"PR{today}{seq:03d}"