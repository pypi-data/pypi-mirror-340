from mcp.server.fastmcp import FastMCP
from markitdown import MarkItDown
mcp = FastMCP('markdownify-mcp-server')
# youtube-to-markdown: Convert YouTube videos to Markdown
# pdf-to-markdown: Convert PDF files to Markdown
# bing-search-to-markdown: Convert Bing search results to Markdown
# webpage-to-markdown: Convert web pages to Markdown
# image-to-markdown: Convert images to Markdown with metadata
# audio-to-markdown: Convert audio files to Markdown with transcription
# docx-to-markdown: Convert DOCX files to Markdown
# xlsx-to-markdown: Convert XLSX files to Markdown
# pptx-to-markdown: Convert PPTX files to Markdown
# get-markdown-file: Retrieve an existing Markdown file

# https://github.com/zcaceres/markdownify-mcp/blob/main/src/tools.ts
# https://github.com/microsoft/markitdown/blob/main/packages/markitdown-mcp/src/markitdown_mcp/__main__.py
@mcp.tool('youtube-to-markdown')
def youtube_to_markdown(filepath:str)->str:
    """Convert a YouTube video to markdown, including transcript if available"""
    return MarkItDown().convert_local(filepath).markdown

@mcp.tool('pdf-to-markdown')
def pdf_to_markdown(filepath:str):
    """Convert a PDF file to markdown"""
    return MarkItDown().convert_local(filepath).markdown

@mcp.tool('bing-search-to-markdown')
def bing_search_to_markdown(url:str):
    """Convert a Bing search results page to markdown"""
    return MarkItDown().convert_url(url).markdown
@mcp.tool('webpage-to-markdown')
def webpage_to_markdown(url : str):
    """Convert a webpage to markdown"""
    return MarkItDown().convert_url(url).markdown
    #convert_local
@mcp.tool('image-to-markdown')
def image_to_markdown(filepath:str):
    """Convert an image to markdown, including metadata and description"""
    return MarkItDown().convert_local(filepath).markdown

@mcp.tool('audio-to-markdown')
def audio_to_markdown(filepath:str):
    """Convert an audio file to markdown, including transcription if possible"""
    return MarkItDown().convert_local(filepath).markdown

@mcp.tool('docx-to-markdown')
def docx_to_markdown(filepath:str):
    """Convert a DOCX file to markdown"""
    return MarkItDown().convert_local(filepath).markdown

@mcp.tool('xlsx-to-markdown')
def xlsx_to_markdown(filepath:str):
    """Convert an XLSX file to markdown"""
    return MarkItDown().convert_local(filepath).markdown

@mcp.tool('pptx-to-markdown')
def pptx_to_markdown(filepath:str):
    """Convert a PPTX file to markdown"""
    return MarkItDown().convert_local(filepath).markdown

@mcp.tool('get-markdown-file')
def get_markdown_file(filepath:str)->str:
    """Get a markdown file by absolute file path"""
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f'文件 {filepath} 未找到。'
    except PermissionError:
        return f'没有权限读取文件 {filepath}。'
    except IOError as e:
        return f'读取文件 {filepath} 时发生错误: {e}'
    
def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()


