from argparse import ArgumentParser as Parser
import aws_s3_util
import database_util


def main():
    parser = Parser()
    parser.add_argument("ticker", help="종목")
    parser.add_argument("date", help="날짜(YYYY-MM-DDTHH:mm)")
    args = parser.parse_args()
    data = aws_s3_util.get_json_data(args.date, args.ticker)
    loadToTable = database_util.JsonToDatabase(data=data, ticker=args.ticker)
    loadToTable.load()


if __name__ == "__main__":
    main()
