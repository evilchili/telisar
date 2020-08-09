from telisar.languages.base import BaseLanguage


class Halfling(BaseLanguage):

    vowels = ["a'", "e'", "i'" "o'", 'a', 'e', 'i', 'o', 'y']
    consonants = ['b', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'z']
    affixes = []

    first_vowels = vowels
    first_consonants = consonants
    first_affixes = affixes

    last_vowels = ['a', 'e', 'i', 'o', 'y']
    last_consonants = consonants
    last_affixes = affixes

    syllable_template = ('c', 'V')
    syllable_weights = [0, 1, 2, 3, 2, 1]

    nicknames = [
        'able', 'clean', 'enthusiastic', 'heartening', 'meek', 'reasonable', 'talented',
        'accommodating', 'clever', 'ethical', 'helpful', 'meritorious', 'refined', 'temperate',
        'accomplished', 'commendable', 'excellent', 'moral', 'reliable', 'terrific',
        'adept', 'compassionate', 'exceptional', 'honest', 'neat', 'remarkable', 'tidy',
        'admirable', 'composed', 'exemplary', 'honorable', 'noble', 'resilient', 'quality',
        'agreeable', 'considerate', 'exquisite', 'hopeful', 'obliging', 'respectable', 'tremendous',
        'amazing', 'consummate', 'extraordinary', 'humble', 'observant', 'respectful', 'trustworthy',
        'appealing', 'cooperative', 'fabulous', 'important', 'optimistic', 'resplendent', 'trusty',
        'astute', 'correct', 'faithful', 'impressive', 'organized', 'responsible', 'truthful',
        'attractive', 'courageous', 'fantastic', 'incisive', 'outstanding', 'robust', 'unbeatable',
        'awesome', 'courteous', 'fascinating', 'incredible', 'peaceful', 'selfless', 'understanding',
        'beautiful', 'dazzling', 'fine', 'innocent', 'perceptive', 'sensational', 'unequaled',
        'benevolent', 'decent', 'classy', 'insightful', 'perfect', 'sensible', 'unparalleled',
        'brave', 'delightful', 'fortitudinous', 'inspiring', 'pleasant', 'serene', 'upbeat',
        'breathtaking', 'dependable', 'gallant', 'intelligent', 'pleasing', 'sharp', 'valiant',
        'bright', 'devoted', 'generous', 'joyful', 'polite', 'shining', 'valuable',
        'brilliant', 'diplomatic', 'gentle', 'judicious', 'positive', 'shrewd', 'vigilant',
        'bubbly', 'discerning', 'gifted', 'just', 'praiseworthy', 'smart', 'vigorous',
        'buoyant', 'disciplined', 'giving', 'kindly', 'precious', 'sparkling', 'virtuous',
        'calm', 'elegant', 'gleaming', 'laudable', 'priceless', 'spectacular', 'well mannered',
        'capable', 'elevating', 'glowing', 'likable', 'principled', 'splendid', 'wholesome',
        'charitable', 'enchanting', 'good', 'lovable', 'prompt', 'steadfast', 'wise',
        'charming', 'encouraging', 'gorgeous', 'lovely', 'prudent', 'stunning', 'witty',
        'chaste', 'endearing', 'graceful', 'loyal', 'punctual', 'super', 'wonderful',
        'cheerful', 'energetic', 'gracious', 'luminous', 'pure', 'superb', 'worthy',
        'chivalrous', 'engaging', 'great', 'magnanimous', 'quick', 'superior', 'zesty',
        'gallant', 'enhanced', 'happy', 'magnificent', 'radiant', 'supportive',
        'civil', 'enjoyable', 'hardy', 'marvelous', 'rational', 'supreme'
    ]

    def person(self):
        return (self.word(), self.word(), self.word())
