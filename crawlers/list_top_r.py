import sys
import argparse
import asyncio
  
from reddit import get_subreddits 

# ------------------------------------------------------------------------------
def main(argv):
    '''Main entry function, called at the beginning of this script.

    Parameters
    ----------
        argv (list). List of string arguments received from the command line.

    Returns
    -------
        status (int). Status code to be returned to the command line. A negative
        value indicates an error, and 0 indicates success.
    '''
    args = parseCommandLine(argv)
    data = asyncio.run(get_subreddits(args.subreddits, args.limit, args.min_score))
    
    print('=' * 80)
    print(f'TOP THREADS ON REDDIT TODAY (limiting in {args.limit} threads with '
          f'minimum score of {args.min_score})')
    print('=' * 80)

    for item in data:
        print(f'SUBREDDIT: {item["subreddit"]}')
        print('')

        if len(item['threads']) > 0:
            for thread in item['threads']:
                print(f'\tURL: {thread["url"]}')
                print(f'\tTITLE: {thread["title"]}')
                print(f'\tSCORE: {thread["score"]}')
                print(f'\tUP VOTES: {thread["ups"]}')
                print(f'\tDOWN VOTES: {thread["downs"]}')
                print(f'\tAUTHOR: {thread["author"]}')
                print(f'\tNUMBER OF COMMENTS: {thread["num_comments"]}')
                print(f'\tCOMMENTS URL: {thread["url_comments"]}')
                print('')
        else:
            print('\tThere are no threads in the query conditions (i.e. limit '
                  'and minimum score)')
            print('')

    print('=' * 80)

    return 0

#---------------------------------------------
def parseCommandLine(argv):
    '''Parses the command line of this script.
    This function uses the argparse package to handle the command line
    arguments. In case of command line errors, the application will be
    automatically terminated.

    Parameters
    ----------
        argv (list). List of strings with the arguments received from the 
        command line.

    Returns
    -------
        args (object). Object with the parsed arguments as attributes
        (refer to the documentation of the argparse package for details).
    '''
    parser = argparse.ArgumentParser(description='Lists the top reddit threads '
                                    'for the given subreddits. Created by Luiz '
                                    'C. Vieira for the IDWall Challenge (2018).')

    parser.add_argument('-s', '--subreddits', metavar='"name[;name;...]"',
                        help='Semicolon-separated list of subreddit names to '
                        'query. IMPORTANT: The quotes are mandatory if you are '
                        'providing more than one name, since the semicolons '
                        'will be understood by the command line processor as '
                        'separators for different commands.', required=True)

    parser.add_argument('-l', '--limit', metavar='value', default=50, type=int,
                        help='Limit of threads to get for each subreddit. '
                        'The default value is 50, and the minimum acceptable '
                        'value is 1.')

    parser.add_argument('-m', '--min_score', metavar='value', default=5000,
                        type=int, help='Minimum score for threads to be '
                        'considered as top, besides the indication of reddit '
                        'itself. The default value is 5000, and the minimum '
                        'acceptable value is 0 (case in which this argument is '
                        'disconsidered).')


    args = parser.parse_args()

    if args.limit <= 0:
        parser.error('The minimum limit of threads to get is 1')

    args.subreddits = args.subreddits.split(';')

    return args

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))