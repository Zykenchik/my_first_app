import re

def normalize_supabase_url(url):
    if not url:
        return url
    
    if url.startswith('https://'):
        return url
    
    if 'postgresql://' in url or 'postgres://' in url:
        match = re.search(r'postgres\.([a-zA-Z0-9]+)', url)
        if match:
            project_ref = match.group(1)
            return f'https://{project_ref}.supabase.co'
        else:
            raise ValueError(f"Cannot extract Supabase project reference from PostgreSQL URL: {url}")
    
    return url
