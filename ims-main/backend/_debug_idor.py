"""临时调试：运行 IDOR 测试并打印响应详情。"""
import pytest
import sys
sys.exit(pytest.main(["-xvs", "--tb=long", "tests/security/test_idor_self_owned.py::TestIdorSelfOwnedData::test_engineer_cannot_view_other_engineer_return_detail"]))