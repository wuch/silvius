# Parser, based on John Aycock's SPARK examples

from spark import GenericParser
from spark import GenericASTBuilder
from ast import AST

class GrammaticalError(Exception):
    def __init__(self, string):
        self.string = string
    def __str__(self):
        return self.string

class CoreParser(GenericParser):
    def __init__(self, start):
        GenericParser.__init__(self, start)

    def typestring(self, token):
        return token.type

    def error(self, token):
        raise GrammaticalError(
            "Unexpected token `%s' (word number %d)" % (token, token.wordno))

    def p_chained_commands(self, args):
        '''
            chained_commands ::= single_command
            chained_commands ::= single_command chained_commands
        '''
        if(len(args) == 1):
            return AST('chain', None, [ args[0] ])
        else:
            args[1].children.insert(0, args[0])
            return args[1]

    def p_single_command(self, args):
        '''
            single_command ::= letter
            single_command ::= sky_letter
            single_command ::= number_rule
            single_command ::= movement
            single_command ::= character
            single_command ::= editing
            single_command ::= modifiers
            single_command ::= english
            single_command ::= word_sentence
            single_command ::= word_variable
            single_command ::= word_phrase
        '''
        return args[0]

    def p_movement(self, args):
        '''
            movement ::= up     repeat
            movement ::= down   repeat
            movement ::= left   repeat
            movement ::= right  repeat
        '''
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('movement', [ args[0] ])
            ])
        else:
            return AST('movement', [ args[0] ])

    def p_repeat(self, args):
        '''
            repeat ::=
            repeat ::= number_set
        '''
        if len(args) > 0:
            return args[0]
        else:
            return None

    small_numbers = {
        'zero'      : 0,
        'one'       : 1,
        'two'       : 2,
        'three'     : 3,
        'four'      : 4,
        'five'      : 5,
        'six'       : 6,
        'seven'     : 7,
        'eight'     : 8,
        'nine'      : 9,
        'ten'       : 10,
        'eleven'    : 11,
        'twelve'    : 12,
        'thirteen'  : 13,
        'fourteen'  : 14,
        'fifteen'   : 15,
        'sixteen'   : 16,
        'seventeen' : 17,
        'eighteen'  : 18,
        'nineteen'  : 19,

        # sadly, kaldi often recognizes these by accident
        'to'        : 2,
        'for'       : 4,
    }
    def p_number_rule(self, args):
        '''
            number_rule ::= number number_set
            number_rule ::= number thousand_number_set
            number_rule ::= number million_number_set
            number_rule ::= number billion_number_set
        '''
        return AST('sequence', [ str(args[1]) ])
    def p_number_set(self, args):
        '''
            number_set ::= _firstnumbers
            number_set ::= _tens
            number_set ::= _tens _ones
            number_set ::= _hundreds
            number_set ::= _hundreds _firstnumbers
            number_set ::= _hundreds _tens
            number_set ::= _hundreds _tens _ones
        '''
        return sum(args)
    def p__ones(self, args):
        '''
            _ones ::= one
            _ones ::= two
            _ones ::= three
            _ones ::= four
            _ones ::= five
            _ones ::= six
            _ones ::= seven
            _ones ::= eight
            _ones ::= nine
            _ones ::= to
            _ones ::= for
        '''
        return self.small_numbers[args[0].type]
    def p__firstnumbers(self, args):
        '''
            _firstnumbers ::= zero
            _firstnumbers ::= one
            _firstnumbers ::= two
            _firstnumbers ::= three
            _firstnumbers ::= four
            _firstnumbers ::= five
            _firstnumbers ::= six
            _firstnumbers ::= seven
            _firstnumbers ::= eight
            _firstnumbers ::= nine
            _firstnumbers ::= ten
            _firstnumbers ::= eleven
            _firstnumbers ::= twelve
            _firstnumbers ::= thirteen
            _firstnumbers ::= fourteen
            _firstnumbers ::= fifteen
            _firstnumbers ::= sixteen
            _firstnumbers ::= seventeen
            _firstnumbers ::= eighteen
            _firstnumbers ::= nineteen
            _firstnumbers ::= to
            _firstnumbers ::= for
        '''
        return self.small_numbers[args[0].type]
    def p__tens(self, args):
        '''
            _tens ::= twenty
            _tens ::= thirty
            _tens ::= forty
            _tens ::= fifty
            _tens ::= sixty
            _tens ::= seventy
            _tens ::= eighty
            _tens ::= ninety
        '''
        value = {
            'twenty'   : 20,
            'thirty'   : 30,
            'forty'    : 40,
            'fifty'    : 50,
            'sixty'    : 60,
            'seventy'  : 70,
            'eighty'   : 80,
            'ninety'   : 90
        }
        return value[args[0].type]
    def p__hundreds(self, args):
        '''
            _hundreds ::= _ones hundred
        '''
        return args[0] * 100
    def p_thousand_number_set(self, args):
        '''
            thousand_number_set ::= number_set thousand
            thousand_number_set ::= number_set thousand number_set
        '''
        total = args[0] * 1000
        if len(args) > 2: total += args[2]
        return total
    def p_million_number_set(self, args):
        '''
            million_number_set ::= number_set million
            million_number_set ::= number_set million number_set
            million_number_set ::= number_set million thousand_number_set
        '''
        total = args[0] * 1000000
        if len(args) > 2: total += args[2]
        return total
    def p_billion_number_set(self, args):
        '''
            billion_number_set ::= number_set billion
            billion_number_set ::= number_set billion number_set
            billion_number_set ::= number_set billion thousand_number_set
            billion_number_set ::= number_set billion million_number_set
        '''
        total = args[0] * 1000000000
        if len(args) > 2: total += args[2]
        return total

    def p_sky_letter(self, args):
        '''
            sky_letter ::= sky letter
        '''
        ast = args[1]
        ast.meta[0] = ast.meta[0].upper()
        return ast

    def p_letter(self, args):
        '''
            letter ::= arch
            letter ::= bravo
            letter ::= charlie
            letter ::= delta
            letter ::= eco
            letter ::= echo
            letter ::= ergo
            letter ::= fox
            letter ::= golf
            letter ::= hotel
            letter ::= india
            letter ::= julia
            letter ::= kilo
            letter ::= line
            letter ::= mike
            letter ::= november
            letter ::= oscar
            letter ::= papa
            letter ::= queen
            letter ::= romeo
            letter ::= sierra
            letter ::= tango
            letter ::= uniform
            letter ::= victor
            letter ::= whiskey
            letter ::= whisky
            letter ::= xray
            letter ::= expert
            letter ::= yankee
            letter ::= zulu
        '''
        if(args[0].type == 'expert'): args[0].type = 'x'
        return AST('char', [ args[0].type[0] ])

    def p_character(self, args):
        '''
            character ::= act
            character ::= colon
            character ::= semicolon
            character ::= single quote
            character ::= double quote
            character ::= equal
            character ::= space
            character ::= tab
            character ::= bang
            character ::= hash
            character ::= dollar
            character ::= percent
            character ::= carrot
            character ::= ampersand
            character ::= star
            character ::= late
            character ::= len
            character ::= rate
            character ::= lack
            character ::= left square
            character ::= minus
            character ::= dash
            character ::= underscore
            character ::= plus
            character ::= backslash
            character ::= dot
            character ::= dit
            character ::= slash
            character ::= question
            character ::= comma
        '''
        value = {
            'act'   : 'Escape',
            'colon' : 'colon',
            'semicolon' : 'semicolon',
            'single': 'apostrophe',
            'double': 'quotedbl',
            'equal' : 'equal',
            'space' : 'space',
            'tab'   : 'Tab',
            'bang'  : 'exclam',
            'hash'  : 'numbersign',
            'dollar': 'dollar',
            'percent': 'percent',
            'carrot': 'caret',
            'ampersand': 'ampersand',
            'star': 'asterisk',
            'late': 'parenleft',
            'len': 'parenleft',
            'rate': 'parenright',
            'lack': 'curlleft',
            'left': 'leftsquare',
            'minus': 'minus',
            'dash': 'minus',
            'underscore': 'underscore',
            'plus': 'plus',
            'backslash': 'backslash',
            'dot': 'period',
            'dit': 'period',
            'slash': 'slash',
            'question': 'question',
            'comma': 'comma'
        }
        return AST('raw_char', [ value[args[0].type] ])

    def p_editing(self, args):
        '''
            editing ::= slap        repeat
            editing ::= scratch     repeat
        '''
        value = {
            'slap'  : 'Return',
            'scratch': 'BackSpace'
        }
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('raw_char', [ value[args[0].type] ])
            ])
        else:
            return AST('raw_char', [ value[args[0].type] ])

    def p_modifiers(self, args):
        '''
            modifiers ::= control single_command
            modifiers ::= alt single_command
            modifiers ::= alternative single_command
            modifiers ::= super single_command
            modifiers ::= shift single_command
            modifiers ::= command single_command
        '''
        value = {
            'control' : 'ctrl',
            'alt' : 'alt',
            'alternative' : 'alt',
            'super' : 'Super_L',
            'shift' : 'Shift_L',
            'command' : 'cmd'
        }
        if(args[1].type == 'mod_plus_key'):
            args[1].meta.insert(0, value[args[0].type])
            return args[1]
        else:
            return AST('mod_plus_key', [ value[args[0].type] ], [ args[1] ] )

    def p_english(self, args):
        '''
            english ::= word ANY
        '''
        return AST('sequence', [ args[1].extra ])

    def p_word_sentence(self, args):
        '''
            word_sentence ::= sentence word_repeat
        '''
        if(len(args[1].children) > 0):
            args[1].children[0].meta = args[1].children[0].meta.capitalize()
        return args[1]

    def p_word_variable(self, args):
        '''
            word_variable ::= variable word_repeat
        '''
        if(len(args[1].children) > 0):
            args[1].children[0].meta = args[1].children[0].meta.capitalize()
        print('TEST: ' + str(args))
        return args[1]


    def p_word_phrase(self, args):
        '''
            word_phrase ::= phrase word_repeat
        '''
        return args[1]

    def p_word_repeat(self, args):
        '''
            word_repeat ::= raw_word
            word_repeat ::= raw_word word_repeat
        '''
        if(len(args) == 1):
            return AST('word_sequence', None,
                [ AST('null', args[0]) ])
        else:
            args[1].children.insert(0, AST('null', args[0]))
            return args[1]

    def p_raw_word(self, args):
        '''
            raw_word ::= ANY
            raw_word ::= zero
            raw_word ::= one
            raw_word ::= two
            raw_word ::= three
            raw_word ::= four
            raw_word ::= five
            raw_word ::= six
            raw_word ::= seven
            raw_word ::= eight
            raw_word ::= nine
            raw_word ::= to
            raw_word ::= for
        '''
        if(args[0].type == 'ANY'):
            return args[0].extra
        return args[0].type

class SingleInputParser(CoreParser):
    def __init__(self):
        # if you have the issue that commands fail because spurious
        # tokens ('i', 'the',...) are prepended to the acual command,
        # try commenting the 'single_input' line, and uncommenting
        # the 'single_input_discard_junk' line.
        CoreParser.__init__(self, 'single_input')
        #CoreParser.__init__(self, 'single_input_discard_junk')
        self.sleeping = False

    def p_sleep_commands(self, args):
        '''
            sleep_commands ::= go to sleep
            sleep_commands ::= start listening
        '''
        if args[-1].type == 'sleep':
            self.sleeping = True
            print 'Going to sleep.'
        else:
            self.sleeping = False
            print 'Waking from sleep'
        return AST('')

    def p_single_input(self, args):
        '''
            single_input ::= END
            single_input ::= sleep_commands END
            single_input ::= chained_commands END
        '''
        if len(args) > 0 and not self.sleeping:
            return args[0]
        else:
            return AST('')

    def p_single_input_discard_junk(self, args):
        '''
            single_input_discard_junk ::= END
            single_input_discard_junk ::= junk_tokens sleep_commands END
            single_input_discard_junk ::= junk_tokens chained_commands END
        '''
        if len(args) > 1 and not self.sleeping:
            return args[1]
        else:
            return AST('')

    # With some models, Kaldi may return spurious tokens in response
    # to noise. If that happens just before we say a command, it will
    # make the command fail. This "dummy" rule will swallows these tokens.
    def p_junk_tokens(self, args):
        '''
            junk_tokens ::=
            junk_tokens ::= i junk_tokens
            junk_tokens ::= the junk_tokens
            junk_tokens ::= a junk_tokens
            junk_tokens ::= and junk_tokens
        '''
        return AST('')


def parse(parser, tokens):
    return parser.parse(tokens)
