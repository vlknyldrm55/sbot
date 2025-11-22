import requests
import re
import urllib3
import warnings

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

class sbot_M3U_Generator:
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
        print("🔍 Getting Selcuksports streams...")

        # Sabit domain
        active_domain = "https://www.selcuksportshda8be70c36d.xyz/"
        print(f"✅ Selcuksports aktif domain: {active_domain}")

        domain_html = self.get_html(active_domain)
        if not domain_html:
            print("❌ Selcuksports domain sayfası alınamadı")
            return 0

        player_links = re.findall(r'data-url="(https?://[^"]+id=[^"]+)"', domain_html)
        if not player_links:
            print("❌ Selcuksports player linkleri bulunamadı")
            return 0

        channel_ids = [
            "selcukbeinsports1", "selcukbeinsports2", "selcukbeinsports3",
            "selcukbeinsports4", "selcukbeinsports5", "selcukbeinsportsmax1",
            "selcukbeinsportsmax2", "selcukssport", "selcukssport2",
            "selcuksmartspor", "selcuksmartspor2", "selcuktivibuspor1",
            "selcuktivibuspor2", "selcuktivibuspor3", "selcuktivibuspor4"
        ]

        found_channels = 0
        for player_url in player_links:
            html_player = self.get_html(player_url)
            if html_player:
                stream_match = re.search(r'this\.baseStreamUrl\s*=\s*[\'"](https://[^\'"]+)[\'"]', html_player)
                if stream_match:
                    base_stream_url = stream_match.group(1)
                    for cid in channel_ids:
                        stream_url = base_stream_url + cid + "/playlist.m3u8"
                        channel_name = "TR:" + cid.upper()
                        self.m3u_content += f'#EXTINF:-1 group-title="Selcuksports",{channel_name}\n'
                        self.m3u_content += f'#EXTVLCOPT:http-referrer={active_domain}\n'
                        self.m3u_content += f'{stream_url}\n'
                        found_channels += 1
                        print(f"✅ Selcuksports: {channel_name}")
                    break

        print(f"📊 Selcuksports: {found_channels} kanal eklendi")
        return found_channels

    def birazcikspor_streams(self):
        print("\n🔍 Scanning Birazcikspor...")

        active_domain = None
        for i in range(42, 200):
            url = f"https://birazcikspor{i}.xyz/"
            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    active_domain = url
                    break
            except:
                continue

        if not active_domain:
            print("❌ Birazcikspor: No active domain found")
            return 0

        try:
            response = requests.get(active_domain, timeout=10)
            html = response.text
        except:
            print("❌ Birazcikspor: Main page not accessible")
            return 0

        first_id_match = re.search(r'<iframe[^>]+id="matchPlayer"[^>]+src="event\.html\?id=([^"]+)"', html)
        first_id = first_id_match.group(1) if first_id_match else None

        base_url = ""
        if first_id:
            try:
                event_response = requests.get(f"{active_domain}event.html?id={first_id}", timeout=10)
                event_source = event_response.text
                base_url_match = re.search(r'var\s+baseurls\s*=\s*\[\s*"([^"]+)"', event_source)
                base_url = base_url_match.group(1) if base_url_match else ""
            except:
                pass

        if not base_url:
            print("❌ Birazcikspor: Base URL not found")
            return 0

        channels = [
            ["beIN Sport 1 HD", "androstreamlivebs1"],
            ["beIN Sport 2 HD", "androstreamlivebs2"],
            ["beIN Sport 3 HD", "androstreamlivebs3"],
            ["beIN Sport 4 HD", "androstreamlivebs4"],
            ["beIN Sport 5 HD", "androstreamlivebs5"],
            ["beIN Sport Max 1 HD", "androstreamlivebsm1"],
            ["beIN Sport Max 2 HD", "androstreamlivebsm2"],
            ["S Sport 1 HD", "androstreamlivess1"],
            ["S Sport 2 HD", "androstreamlivess2"],
            ["Tivibu Sport HD", "androstreamlivets"],
        ]

        successful_channels = 0
        for channel in channels:
            stream_url = f"{base_url}{channel[1]}.m3u8"
            try:
                response = requests.head(stream_url, timeout=5)
                if response.status_code == 200:
                    self.m3u_content += f'#EXTINF:-1 group-title="Birazcikspor",{channel[0]}\n'
                    self.m3u_content += f"{stream_url}\n"
                    successful_channels += 1
                    print(f"✅ Birazcikspor: {channel[0]}")
                else:
                    print(f"❌ Birazcikspor: {channel[0]}")
            except:
                print(f"❌ Birazcikspor: {channel[0]}")

        print(f"📊 Birazcikspor: {successful_channels} kanal eklendi")
        return successful_channels

    def save_m3u(self):
        file_path = "sbot.m3u"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.m3u_content)
            print(f"\n💾 M3U file saved: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Save error: {str(e)}")
            return False

def main():
    print("🚀 Starting sbot Multi-Source Bot...")
    generator = sbot_M3U_Generator()

    total_channels = 0
    total_channels += generator.selcuksports_streams()
    total_channels += generator.birazcikspor_streams()

    if total_channels > 0:
        generator.save_m3u()
        print(f"\n🎯 Process completed! Total channels: {total_channels}")
    else:
        print("💥 No channels found from any source!")

if __name__ == "__main__":
    main()
