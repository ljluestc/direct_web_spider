# encoding: utf-8
import requests
import re
from spider.fetcher import Fetcher


class TmallFetcher(Fetcher):
    """
    Fetcher for Tmall (tmall.com) e-commerce site
    """
    URL = "http://www.tmall.com/go/rgn/mall/iwanttobuy-data.php?d=20110910"

    # Blacklist of problematic URLs to skip
    BLACK_LIST = [
        "http://list.tmall.com/50025135/g,guydamrvge2dkorxga4tmmbmguydamrzgyzdoorwgyzdmnjmguydamrvg44dgorugmzdsnzmguydamrvgi3dkorshe2tiojmguydamrvg44diorugyytinzmguydamrvg44dsorsga4tcnjmguydamrvg44dqorsgeztgnbmguydamrvgizdoorsgi3tkojmguydamrvgi3dgorrge4dcojmguydamrvgi2tqortge4tonjmguydamrvgi3teorygi2tolbvgaydenjsgy3dumzvgu2dglbvgaydenjsgmztunrwgizcynjqgaztcmzzg45dcmbsgy4cynjqga2dqnrsha5dsmzugywdkmbqgi2toobxhiytinjqgiwdkmbqgi2tqmrrhizdenjqgywdkmbqgi3tenbthiztenrzfq2tambsguytkmr2gy3tanrmguydanbxge3daorsguytanrmguydanbxgm2tmorrha3dsmzmguydanbxgm2toorrhe4dmnzmguydamrvg44tkoruhe2dklbvgaydenjyga3dumzqge3synjqgazdkobsg45dgmzrgawdkmbqgi2tqmrvhiytcnjsgywdkmbqgi2tqmzxhiytanbxfq2tambwgq3donr2gyztombm--0----------------------g-d-----40-0--50025233-x.htm?is=cate",
        # ... (other blacklist items as shown in Ruby code)
        "http://list.tmall.com/50024897/g-s--99---40-0--50026022-x.htm?TBG=19622.15482.57"
    ]

    @classmethod
    def category_list(cls):
        """
        Fetch category list from Tmall

        Returns:
            list: List of category dicts with 'name' and 'url' keys
        """
        response = requests.get(cls.URL)
        html = response.content.decode('GB18030', errors='replace')

        # Extract all JavaScript objects like ({name:"...", href:"..."})
        pattern = r'\((.*?)\)'
        matches = re.findall(pattern, html)

        categories = []
        for match in matches:
            # Try to parse as Python dict (after cleaning)
            try:
                # Remove "class" property which causes issues
                cleaned = re.sub(r'"class".*?\}', '}', match)

                # Convert JavaScript object to Python dict
                # This is a simple approach - may need refinement
                if 'name' in cleaned and 'href' in cleaned:
                    name_match = re.search(r'name\s*:\s*"([^"]+)"', cleaned)
                    href_match = re.search(r'href\s*:\s*"([^"]+)"', cleaned)

                    if name_match and href_match:
                        name = name_match.group(1)
                        url = href_match.group(1)

                        # Filter valid URLs
                        if (url.startswith('http://list.tmall.com') and
                                'catid_count' not in url and
                                url not in cls.BLACK_LIST):
                            categories.append({
                                'name': name,
                                'url': url
                            })
            except Exception:
                # Skip malformed entries
                pass

        return categories
