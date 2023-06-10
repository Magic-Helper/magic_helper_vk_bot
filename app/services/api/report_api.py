from app.entities import CreateReport, ReportCount
from app.services.api.base import BaseAPI


class ReportAPI(BaseAPI):
    async def create_report(self, author_nickname: str, report_steamid: str, server_number: int) -> None:
        create_report = CreateReport(
            author_nickname=author_nickname, report_steamid=report_steamid, server_number=server_number
        ).dict(exclude_none=True)
        await self.client.api_POST_request('/v1/reports', body=create_report)

    async def get_report_count_per_steamid(self, time_start: int) -> dict[str, int]:
        return await self.client.api_GET_request(f'/v1/reports/{time_start}', response_model=dict)

    async def get_player_reports(self, report_steamid: str, time_start: int) -> ReportCount:
        return await self.client.api_GET_request(
            f'/v1/reports/{report_steamid}/{time_start}', response_model=ReportCount
        )
