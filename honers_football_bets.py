from bs4 import BeautifulSoup
from prettytable import PrettyTable
import requests
import re
import re
import datetime
import time
from colorama import Fore, Style
import argparse
import sys

def check_days_ahead(value) -> int:
    ivalue = int(value)
    if ivalue < 0:
        raise argparse.ArgumentTypeError(f"{value} is negative")
    return ivalue


def check_confidence_threshold(value) -> int:
    ivalue = int(value)
    if ivalue < 0 or ivalue > 41:
        raise argparse.ArgumentTypeError(f"{value} is not valid")
    return ivalue


def momentum(score):
    if score > 14:
        moment = "EXCELLENT"
    elif score > 7:
        moment = "GREAT"
    elif score >= 0:
        moment = "OKAY"
    elif score > -7:
        moment = "BAD"
    elif score > -14:
        moment = "TERRIBLE"
    else:
        moment = "DISGUSTING"

    return moment

def team_moment(team, score, id):
    if score > 14:
        moment = "EXCELLENT"
    elif score > 7:
        moment = "GREAT"
    elif score > 0:
        moment = "OKAY"
    elif score > -7:
        moment = "BAD"
    elif score > -14:
        moment = "TERRIBLE"
    else:
        moment = "DISGUSTING"

    if id == 0:
        print(f"{Fore.CYAN}{team} is in a {moment} moment.{Style.RESET_ALL}")
    else:
        print(f"{Fore.MAGENTA}{team} is in a {moment} moment.{Style.RESET_ALL}")


def bet_confidence(team, score):
    if score >= 35:
        print(f"{Fore.GREEN}Beting on {Style.RESET_ALL}{team}{Fore.GREEN} is FREE MONEY{Style.RESET_ALL}")
    elif score >= 28:
        print(f"{Fore.GREEN}Beting on {Style.RESET_ALL}{team}{Fore.GREEN} is SAFE{Style.RESET_ALL}")
    elif score >= 21:
        print(f"{Fore.GREEN}Beting on {Style.RESET_ALL}{team}{Fore.GREEN} is GREAT{Style.RESET_ALL}")
    elif score >= 14:
        print(f"{Fore.YELLOW}Beting on {Style.RESET_ALL}{team}{Fore.YELLOW} is GOOD{Style.RESET_ALL}")
    elif score >= 7:
        print(f"{Fore.YELLOW}Beting on {Style.RESET_ALL}{team}{Fore.YELLOW} is TOO CLOSE TO CALL{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}This Bet is RISKY{Style.RESET_ALL}")


def main(args):
    parser = argparse.ArgumentParser(description="Honer's Football Bets")
    parser.add_argument(
        "-d",
        "--days",
        action="store",
        dest="days_ahead",
        type=check_days_ahead,
        default=3,
        help="Number of days ahead to get fixtures from.",
    )
    parser.add_argument(
        "-c",
        "--confidence",
        action="store",
        dest="confidence_threshold",
        type=check_confidence_threshold,
        default=0,
        help="Confidence threshold from 0 to 41 to print fixtures.",
    )

    (ns_parser, l_unknown_args) = parser.parse_known_args(args)
    if l_unknown_args:
        print(f"The following args couldn't be interpreted: {l_unknown_args}")

    max_days_to_look = ns_parser.days_ahead
    filter_confidence = ns_parser.confidence_threshold
    l_competitions = [("PREMIER LEAGUE", "https://www.skysports.com/premier-league-fixtures"),
                    ("CHAMPIONSHIP", "https://www.skysports.com/championship-fixtures"),
                    ("LEAGUE ONE", "https://www.skysports.com/league-1-fixtures"),
                    ("LEAGUE TWO", "https://www.skysports.com/league-2-fixtures"),]

    print("")
    print("⚽️ ⚽️ ⚽️ ⚽️ ⚽️ WELCOME TO HONER'S FOOTBALL BETS ⚽️ ⚽️ ⚽️ ⚽️ ⚽️\n")
    print("Configuration")
    print(f"   Days to look for fixtures: {max_days_to_look} ")
    print(f"   Confidence threshold filter: {filter_confidence} ")
    print(f"   Competitions: {', '.join([t_competition[0] for t_competition in l_competitions])}")
    print("")



    dt_game = datetime.datetime.strptime("01 January 2000", "%d %B %Y")

    for competition,url_fixture in l_competitions:
        print(f"💎💎💎 {competition} 💎💎💎\n")

        text_fixtures = BeautifulSoup(requests.get(url_fixture).text, "lxml")
        time.sleep(.2)
        for fixture in text_fixtures.findAll('div', {'class': 'fixres__item'}):
            time.sleep(.2)
            for fix in BeautifulSoup(str(fixture), "lxml").findAll('a', href=True):
                time.sleep(.2)
                if 'skysports' in fix['href']:
                    l_link = fix['href'].rsplit('/',1)
                    url_results = f"{l_link[0]}/stats/{l_link[1]}"

                    text_results = BeautifulSoup(requests.get(url_results).text, "lxml")

                    dt_data = text_results.find('div', {'class': 'sdc-site-match-header__detail'})
                    dt = BeautifulSoup(str(dt_data), "lxml").find('time').next_element.replace(', ', ' ').split()
                    date = " ".join(dt[2:])[:-1]
                    date = date.replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')

                    #dt_game = datetime.datetime.strptime(date, "%d %B %Y")
                    days_till_feature = (datetime.datetime.strptime(date, "%d %B %Y") - datetime.datetime.now()).days + 1

                    if days_till_feature > max_days_to_look:
                        break
                    #print(f"Days until feature: {days_till_feature}")

                    if datetime.datetime.strptime(date, "%d %B %Y") > dt_game:
                        print(f"✨✨✨ {date} ✨✨✨\n")

                    dt_game = datetime.datetime.strptime(date, "%d %B %Y")

                    d_stats = {}
                    for team in url_results.split('/')[-3].split('-vs-'):
                        d_stats[team] = list()

                    for result_data in text_results.findAll('a', {'class': 'sdc-site-last-games__result'}):
                        #print(result_data)
                        time.sleep(0.2)
                        for parts in result_data['href'].split('/'):
                            if 'vs' in parts:
                                teams = parts.split('-vs-')

                        outcome = result_data['data-outcome']
                        result = result_data.find('div', {'class': 'sdc-site-last-games__score'}).text.strip()
                        opponent = re.sub(r"\([^()]*\)", "", result_data.find('span', {'class': 'sdc-site-last-games__opponent'}).text.strip()).strip()
                        homeaway = result_data.find('span', {'class': 'sdc-site-last-games__location'}).text.strip()
                        opponent += " " + homeaway

                        d_stats[teams[0 if homeaway == '(h)' else 1]].append((outcome,result,opponent))

                    #print(d_stats)

                    pt = PrettyTable()
                    pt.field_names = ["Team", "More Recent", "", "    ", "   ", " ", "Older"]

                    l_names = list()
                    l_scores = list()
                    for idx,team in enumerate(d_stats):
                        score = 0
                        l_outcomes = [""]
                        team_name = team.replace('-', ' ').title()
                        if idx == 0:
                            l_names.append(Fore.CYAN + team_name + Style.RESET_ALL)
                            l_results = [Fore.CYAN + team_name + Style.RESET_ALL]
                        else:
                            l_names.append(Fore.MAGENTA + team_name + Style.RESET_ALL)
                            l_results = [Fore.MAGENTA + team_name + Style.RESET_ALL]

                        l_opponents = [""]
                        for idx,out in enumerate(d_stats[team]):
                            if out[0] == 'win':
                                l_outcomes.append(Fore.GREEN + out[0].upper() + Style.RESET_ALL)
                                score += (6-idx)
                            elif out[0] == 'lose':
                                l_outcomes.append(Fore.RED + out[0].upper() + Style.RESET_ALL)
                                score -= (6-idx)
                            else:
                                l_outcomes.append(Fore.YELLOW + out[0].upper() + Style.RESET_ALL)
                            l_results.append(out[1])
                            l_opponents.append(out[2])
                        if score >= 7:
                            l_opponents[0] = f"{Fore.GREEN}{momentum(score)} ({score}){Style.RESET_ALL}"
                        elif score <= -7:
                            l_opponents[0] = f"{Fore.RED}{momentum(score)} ({score}){Style.RESET_ALL}"
                        else:
                            l_opponents[0] = f"{Fore.YELLOW}{momentum(score)} ({score}){Style.RESET_ALL}"
                        l_scores.append(score)
                        pt.add_row(l_outcomes)
                        pt.add_row(l_results)
                        pt.add_row(l_opponents)
                        pt.add_row(['', '', '', '', '', '', ''])

                    confidence = abs(l_scores[1]-l_scores[0])
                    if confidence > filter_confidence:
                        print(f"{' '.join(dt[:2])} {date} - {competition}")
                        bet_confidence((l_names[0], l_names[1])[l_scores[1]>l_scores[0]], confidence)
                        #for idx,(nam,sc) in enumerate(zip(l_names, l_scores)):
                        #    team_moment(nam, sc, idx)
                        print(pt)
                        print("\n")

            if days_till_feature > max_days_to_look:
                break

if __name__ == '__main__':
    main(sys.argv[1:])