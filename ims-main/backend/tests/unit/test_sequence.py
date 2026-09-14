"""
单据编号生成测试。
验证所有前缀的编号格式和按日递增逻辑。
"""

import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app.utils.order_no import (
    _next_seq,
    generate_inbound_no,
    generate_outbound_no,
    generate_rc_no,
    generate_inspection_no,
    generate_return_no,
    generate_fc_no,
    generate_diag_no,
    generate_repair_no,
    generate_scrap_no,
    generate_reship_no,
    generate_shipment_no,
    generate_bom_no,
    generate_task_no,
)


class TestSequenceGeneration:
    """编号生成测试"""

    def test_jin_prefix_format(self, db_session: Session):
        """JIN入库单号格式：JIN-{YYYYMMDD}-{序号4位}。"""
        no = generate_inbound_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("JIN-")
        assert today in no
        assert len(no.split("-")[2]) == 4

    def test_jout_prefix_format(self, db_session: Session):
        """JOUT出库单号格式：JOUT-{YYYYMMDD}-{序号4位}。"""
        no = generate_outbound_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("JOUT-")
        assert today in no
        assert len(no.split("-")[2]) == 4

    def test_rc_prefix_format(self, db_session: Session):
        """RC到货单号格式：RC{YYYYMMDD}{序号3位}。"""
        no = generate_rc_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("RC")
        assert today in no

    def test_jc_prefix_format(self, db_session: Session):
        """JC检验编号格式：JC{YYYYMMDD}{序号3位}。"""
        no = generate_inspection_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("JC")
        assert today in no

    def test_th_prefix_format(self, db_session: Session):
        """TH退货单号格式：TH{YYYYMMDD}{序号3位}。"""
        no = generate_return_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("TH")
        assert today in no

    def test_fc_prefix_format(self, db_session: Session):
        """FC返厂单号格式：FC{YYYYMMDD}{序号3位}。"""
        no = generate_fc_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("FC")
        assert today in no

    def test_dg_prefix_format(self, db_session: Session):
        """DG诊断编号格式：DG{YYYYMMDD}{序号3位}。"""
        no = generate_diag_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("DG")
        assert today in no

    def test_wx_prefix_format(self, db_session: Session):
        """WX维修工单号格式：WX{YYYYMMDD}{序号3位}。"""
        no = generate_repair_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("WX")
        assert today in no

    def test_bf_prefix_format(self, db_session: Session):
        """BF报废单号格式：BF{YYYYMMDD}{序号3位}。"""
        no = generate_scrap_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("BF")
        assert today in no

    def test_rh_prefix_format(self, db_session: Session):
        """RH再出货单号格式：RH{YYYYMMDD}{序号3位}。"""
        no = generate_reship_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("RH")
        assert today in no

    def test_sh_prefix_format(self, db_session: Session):
        """SH出货单号格式：SH{YYYYMMDD}{序号3位}。"""
        no = generate_shipment_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("SH")
        assert today in no

    def test_bom_prefix_format(self, db_session: Session):
        """BOM编号格式：BOM{YYYYMMDD}{序号3位}。"""
        no = generate_bom_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("BOM")
        assert today in no

    def test_pr_prefix_format(self, db_session: Session):
        """PR生产任务编号格式：PR{YYYYMMDD}{序号3位}。"""
        no = generate_task_no(db_session)
        today = datetime.now().strftime("%Y%m%d")
        assert no.startswith("PR")
        assert today in no

    def test_sequence_increments_within_same_type(self, db_session: Session):
        """同一类型连续生成编号递增。"""
        no1 = generate_rc_no(db_session)
        no2 = generate_rc_no(db_session)
        seq1 = int(no1[-3:])
        seq2 = int(no2[-3:])
        assert seq2 == seq1 + 1, f"序号应递增: {seq1} → {seq2}"

    def test_all_prefixes_generate_unique(self, db_session: Session):
        """所有前缀生成不冲突。"""
        generators = [
            generate_inbound_no, generate_outbound_no, generate_rc_no,
            generate_inspection_no, generate_return_no, generate_fc_no,
            generate_diag_no, generate_repair_no, generate_scrap_no,
            generate_reship_no, generate_shipment_no, generate_bom_no, generate_task_no,
        ]
        results = set()
        for gen in generators:
            no = gen(db_session)
            assert no not in results, f"编号重复: {no}"
            results.add(no)
        assert len(results) == len(generators)