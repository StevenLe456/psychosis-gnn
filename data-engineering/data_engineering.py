import nonpsychotic_author_scraper as nas
import nonpsychotic_post_scraper as nps
import psychotic_author_scraper as pas
import psychotic_post_scraper as pps
import create_graphs as cg

def main(dir):
    nas.main()
    pas.main()
    nps.main()
    pps.main()
    cg.main(dir)