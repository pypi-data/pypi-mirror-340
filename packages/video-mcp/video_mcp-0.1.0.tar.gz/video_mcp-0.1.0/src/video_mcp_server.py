#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from tmdbv3api import TMDb, Movie, TV, Search

# Load environment variables
load_dotenv()

# Initialize TMDB
tmdb = TMDb()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY environment variable is required")

tmdb.api_key = TMDB_API_KEY
tmdb.language = "zh"  # 设置默认语言为中文

# Initialize TMDB clients
movie = Movie()
tv = TV()
search = Search()

# Create FastMCP server instance
mcp = FastMCP("video-mcp-server")

@mcp.tool()
async def search_video(
    query: str,
    media_type: str = "all",
    year: int | None = None,
    page: int = 1
) -> str:
    """搜索电影和电视剧信息
    
    Args:
        query: 搜索关键词
        media_type: 指定搜索类型：movie(电影)、tv(电视剧)或all(全部)
        year: 指定年份进行过滤（可选）
        page: 页码，默认为1
    """
    try:
        results = []
        if media_type in ["movie", "all"]:
            movie_results = movie.search(query)
            for item in movie_results:
                if not year or str(item.release_date).startswith(str(year)):
                    results.append({
                        "id": item.id,
                        "title": item.title,
                        "original_title": item.original_title,
                        "media_type": "movie",
                        "release_date": item.release_date,
                        "overview": item.overview,
                        "poster_path": f"https://image.tmdb.org/t/p/w500{item.poster_path}" if item.poster_path else None,
                        "vote_average": item.vote_average
                    })

        if media_type in ["tv", "all"]:
            tv_results = tv.search(query)
            for item in tv_results:
                if not year or str(item.first_air_date).startswith(str(year)):
                    results.append({
                        "id": item.id,
                        "title": item.name,
                        "original_title": item.original_name,
                        "media_type": "tv",
                        "release_date": item.first_air_date,
                        "overview": item.overview,
                        "poster_path": f"https://image.tmdb.org/t/p/w500{item.poster_path}" if item.poster_path else None,
                        "vote_average": item.vote_average
                    })

        output = f"找到 {len(results)} 个结果：\n\n"
        output += "\n\n".join([
            f"标题: {r['title']}\n"
            f"类型: {'电影' if r['media_type'] == 'movie' else '电视剧'}\n"
            f"发布日期: {r['release_date']}\n"
            f"评分: {r['vote_average']}\n"
            f"简介: {r['overview']}\n"
            f"海报: {r['poster_path']}"
            for r in results
        ])
        return output
    except Exception as e:
        return f"搜索失败: {str(e)}"

@mcp.tool()
async def get_video_details(video_id: int, media_type: str) -> str:
    """获取特定影视作品的详细信息
    
    Args:
        video_id: 影视作品的ID
        media_type: 作品类型：movie(电影)或tv(电视剧)
    """
    try:
        if media_type == "movie":
            details = movie.details(video_id)
            result = {
                "id": details.id,
                "title": details.title,
                "original_title": details.original_title,
                "release_date": details.release_date,
                "overview": details.overview,
                "runtime": details.runtime,
                "genres": [genre.name for genre in details.genres],
                "vote_average": details.vote_average,
                "poster_path": f"https://image.tmdb.org/t/p/w500{details.poster_path}" if details.poster_path else None,
                "production_companies": [company.name for company in details.production_companies],
                "budget": details.budget,
                "revenue": details.revenue
            }
        else:  # tv
            details = tv.details(video_id)
            result = {
                "id": details.id,
                "title": details.name,
                "original_title": details.original_name,
                "first_air_date": details.first_air_date,
                "overview": details.overview,
                "episode_run_time": details.episode_run_time,
                "number_of_seasons": details.number_of_seasons,
                "number_of_episodes": details.number_of_episodes,
                "genres": [genre.name for genre in details.genres],
                "vote_average": details.vote_average,
                "poster_path": f"https://image.tmdb.org/t/p/w500{details.poster_path}" if details.poster_path else None,
                "production_companies": [company.name for company in details.production_companies],
                "status": details.status
            }

        return "详细信息：\n\n" + "\n".join([f"{k}: {v}" for k, v in result.items()])
    except Exception as e:
        return f"获取详情失败: {str(e)}"

def main():
    import asyncio
    asyncio.run(mcp.run())

if __name__ == "__main__":
    main()
