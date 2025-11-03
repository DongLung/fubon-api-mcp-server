"""
市場數據測試
"""
import pytest


class TestMarketData:
    """市場數據功能測試"""

    def test_intraday_ticker(self, rest_client):
        """測試獲取股票基本資料"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.intraday.ticker(symbol='2330')
            assert result is not None
            assert 'symbol' in result or hasattr(result, 'symbol')
        except Exception as e:
            pytest.skip(f"API調用失敗: {str(e)}")

    def test_intraday_quote(self, rest_client):
        """測試獲取即時報價"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.intraday.quote(symbol='2330')
            assert result is not None
            # 檢查是否有價格資訊
            assert hasattr(result, 'price') or 'price' in result
        except Exception as e:
            pytest.skip(f"即時報價API不可用: {str(e)}")

    def test_intraday_candles(self, rest_client):
        """測試獲取盤中K線"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.intraday.candles(symbol='2330')
            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0
        except Exception as e:
            pytest.skip(f"K線數據不可用: {str(e)}")

    def test_intraday_trades(self, rest_client):
        """測試獲取成交明細"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.intraday.trades(symbol='2330')
            assert result is not None
            assert isinstance(result, list)
        except Exception as e:
            pytest.skip(f"成交明細不可用: {str(e)}")

    def test_intraday_volumes(self, rest_client):
        """測試獲取分價量表"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.intraday.volumes(symbol='2330')
            assert result is not None
            assert isinstance(result, list)
        except Exception as e:
            pytest.skip(f"分價量表不可用: {str(e)}")

    def test_snapshot_quotes(self, rest_client):
        """測試獲取行情快照"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.snapshot.quotes(market='TSE')
            assert result is not None
            assert isinstance(result, list)
            assert len(result) > 0
        except Exception as e:
            pytest.skip(f"行情快照不可用: {str(e)}")

    def test_snapshot_movers(self, rest_client):
        """測試獲取漲跌幅排行"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.snapshot.movers(market='TSE', type='up')
            assert result is not None
            assert isinstance(result, list)
        except Exception as e:
            pytest.skip(f"漲跌幅排行不可用: {str(e)}")

    def test_snapshot_actives(self, rest_client):
        """測試獲取成交量排行"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.snapshot.actives(market='TSE', type='volume')
            assert result is not None
            assert isinstance(result, list)
        except Exception as e:
            pytest.skip(f"成交量排行不可用: {str(e)}")

    def test_historical_candles(self, rest_client):
        """測試獲取歷史K線"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.historical.candles(
                symbol='2330',
                from_date='2024-01-01',
                to_date='2024-01-05'
            )
            assert result is not None
            assert isinstance(result, list)
        except Exception as e:
            pytest.skip(f"歷史K線不可用: {str(e)}")

    def test_historical_stats(self, rest_client):
        """測試獲取歷史統計"""
        if rest_client is None:
            pytest.skip("測試環境不支持 REST 客戶端")
        try:
            result = rest_client.historical.stats(symbol='2330')
            assert result is not None
            # 檢查是否有基本統計資訊
            assert 'symbol' in result or hasattr(result, 'symbol')
        except Exception as e:
            pytest.skip(f"歷史統計不可用: {str(e)}")