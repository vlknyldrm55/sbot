import requests
import re
import time
import urllib3
import warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

class M3UGenerator:
    def __init__(self):
        self.m3u_content = "#EXTM3U\n"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36'
        })
    
    def get_html(self, url):
        try:
            response = self.session.get(url, timeout=20, verify=False)
            response.raise_for_status()
            return response.text
        except Exception:
            return None
    
    def selcuksports_streams(self):
        print("Getting Selcuksports streams...")
        
        url = "https://seep.eu.org/https://www.selcuksportshd.is/"
        
        channel_ids = [
            "selcukbeinsports1", "selcukbeinsports2", "selcukbeinsports3",
            "selcukbeinsports4", "selcukbeinsports5", "selcukbeinsportsmax1",
            "selcukbeinsportsmax2", "selcukssport", "selcukssport2",
            "selcuksmartspor", "selcuksmartspor2", "selcuktivibuspor1",
            "selcuktivibuspor2", "selcuktivibuspor3", "selcuktivibuspor4"
        ]
        
        html = self.get_html(url)
        if not html:
            print("Main page not available")
            return
        
        active_domain = ""
        
        section_match = re.search(r'data-device-mobile[^>]*>(.*?)</div>\s*</div>', html, re.DOTALL)
        if section_match:
            link_match = re.search(r'href=["\'](https?://[^"\']*selcuksportshd[^"\']+)["\']', section_match.group(1))
            if link_match:
                active_domain = link_match.group(1)
        
        if not active_domain:
            print("Active domain not found")
            return
        
        print(f"Active domain: {active_domain}")
        
        domain_html = self.get_html(active_domain)
        if not domain_html:
            print("Domain page not available")
            return
        
        player_links = re.findall(r'data-url="(https?://[^"]+id=[^"]+)"', domain_html)
        
        if not player_links:
            print("Player links not found")
            return
        
        found_channels = 0
        
        for player_url in player_links:
            html_player = self.get_html(player_url)
            if html_player:
                stream_match = re.search(r'this\.baseStreamUrl\s*=\s*[\'"](https://[^\'"]+)[\'"]', html_player)
                if stream_match:
                    base_stream_url = stream_match.group(1)
                    
                    for cid in channel_ids:
                        stream_url = base_stream_url + cid + "/playlist.m3u8"
                        
                        clean_name = re.sub(r'^selcuk', '', cid, flags=re.IGNORECASE)
                        clean_name = clean_name.upper() + " HD"
                        channel_name = "TR:" + clean_name
                        
                        self.m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{channel_name}" tvg-logo="https://i.hizliresim.com/b6xqz10.jpg" group-title="TURKIYE",{channel_name}\n'
                        self.m3u_content += f'#EXTVLCOPT:http-referrer={active_domain}\n'
                        self.m3u_content += f'{stream_url}\n'
                        
                        found_channels += 1
                        print(f"Added: {channel_name}")
                    
                    break
        
        print(f"Total channels added: {found_channels}")
    
    def save_m3u(self, filename="DeaTHLesS-Selcuksport.m3u"):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.m3u_content)
            print(f"M3U file saved: {filename}")
        except Exception as e:
            print(f"Save error: {str(e)}")

def main():
    generator = M3UGenerator()
    
    generator.selcuksports_streams()
    
    generator.save_m3u()
    
    print("Process completed")

if __name__ == "__main__":
    main()