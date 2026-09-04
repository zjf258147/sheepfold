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