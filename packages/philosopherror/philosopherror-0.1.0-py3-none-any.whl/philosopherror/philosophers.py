"""
Contains the database of philosophical quotes and error mappings.
"""

# Dictionary of philosophers and their genuine quotes
PHILOSOPHER_QUOTES = {
    # Western Philosophy
    "Socrates": [
        "The only true wisdom is in knowing you know nothing.",
        "The unexamined life is not worth living.",
        "I cannot teach anybody anything. I can only make them think.",
        "Beware the barrenness of a busy life.",
        "By all means, marry. If you get a good wife, you'll become happy; if you get a bad one, you'll become a philosopher.",
        "Wonder is the beginning of wisdom."
    ],
    "Plato": [
        "We can easily forgive a child who is afraid of the dark; the real tragedy of life is when men are afraid of the light.",
        "The measure of a man is what he does with power.",
        "The price good men pay for indifference to public affairs is to be ruled by evil men.",
        "Knowledge becomes evil if the aim be not virtuous.",
        "Good people do not need laws to tell them to act responsibly, while bad people will find a way around the laws.",
        "Only the dead have seen the end of war."
    ],
    "Aristotle": [
        "It is the mark of an educated mind to be able to entertain a thought without accepting it.",
        "Excellence is never an accident. It is always the result of high intention, sincere effort, and intelligent execution.",
        "The whole is greater than the sum of its parts.",
        "Happiness depends upon ourselves.",
        "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
        "The educated differ from the uneducated as much as the living differ from the dead.",
        "Poverty is the parent of revolution and crime."
    ],
    "Marcus Aurelius": [
        "You have power over your mind - not outside events. Realize this, and you will find strength.",
        "The happiness of your life depends upon the quality of your thoughts.",
        "The impediment to action advances action. What stands in the way becomes the way.",
        "Very little is needed to make a happy life; it is all within yourself, in your way of thinking.",
        "Never let the future disturb you. You will meet it, if you have to, with the same weapons of reason which today arm you against the present.",
        "Waste no more time arguing about what a good man should be. Be one."
    ],
    "Epictetus": [
        "It's not what happens to you, but how you react to it that matters.",
        "Make the best use of what is in your power, and take the rest as it happens.",
        "First say to yourself what you would be; and then do what you have to do.",
        "No man is free who is not master of himself.",
        "He who laughs at himself never runs out of things to laugh at.",
        "Don't explain your philosophy. Embody it."
    ],
    "Seneca": [
        "We suffer more often in imagination than in reality.",
        "Luck is what happens when preparation meets opportunity.",
        "Life is long if you know how to use it.",
        "It is not the man who has too little, but the man who craves more, that is poor.",
        "Difficulties strengthen the mind, as labor does the body.",
        "As is a tale, so is life: not how long it is, but how good it is, is what matters.",
        "To err is human, but to persist in error is diabolical."
    ],
    "Nietzsche": [
        "He who has a why to live for can bear almost any how.",
        "That which does not kill us makes us stronger.",
        "There are no facts, only interpretations.",
        "The individual has always had to struggle to keep from being overwhelmed by the tribe.",
        "In individuals, insanity is rare; but in groups, parties, nations and epochs, it is the rule.",
        "Whoever fights monsters should see to it that in the process he does not become a monster."
    ],
    "Kant": [
        "Act only according to that maxim whereby you can, at the same time, will that it should become a universal law.",
        "Science is organized knowledge. Wisdom is organized life.",
        "Dare to know! Have the courage to use your own understanding.",
        "Genius is the ability to independently arrive at and understand concepts that would normally have to be taught by another person.",
        "Live your life as though your every act were to become a universal law.",
        "All our knowledge begins with the senses, proceeds then to the understanding, and ends with reason."
    ],
    "Wittgenstein": [
        "The limits of my language mean the limits of my world.",
        "Whereof one cannot speak, thereof one must be silent.",
        "Philosophy is a battle against the bewitchment of our intelligence by means of language.",
        "A nothing will serve just as well as a something about which nothing can be said.",
        "If people never did silly things, nothing intelligent would ever get done.",
        "Don't think, but look!"
    ],
    "Sartre": [
        "Man is condemned to be free; because once thrown into the world, he is responsible for everything he does.",
        "Hell is other people.",
        "Freedom is what you do with what's been done to you.",
        "Existence precedes essence.",
        "When the rich wage war, it's the poor who die.",
        "Life begins on the other side of despair."
    ],
    "Camus": [
        "The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.",
        "Should I kill myself, or have a cup of coffee?",
        "In the midst of winter, I found there was, within me, an invincible summer.",
        "Nobody realizes that some people expend tremendous energy merely to be normal.",
        "Autumn is a second spring when every leaf is a flower.",
        "Real generosity toward the future lies in giving all to the present."
    ],
    
    # Eastern Philosophy
    "Confucius": [
        "It does not matter how slowly you go as long as you do not stop.",
        "The man who moves a mountain begins by carrying away small stones.",
        "By three methods we may learn wisdom: First, by reflection, which is noblest; Second, by imitation, which is easiest; and third by experience, which is the bitterest.",
        "When anger rises, think of the consequences.",
        "Life is really simple, but we insist on making it complicated.",
        "To know what you know and what you do not know, that is true knowledge.",
        "The superior man is modest in his speech but exceeds in his actions."
    ],
    "Lao Tzu": [
        "The journey of a thousand miles begins with one step.",
        "Knowing others is wisdom, knowing yourself is enlightenment.",
        "Nature does not hurry, yet everything is accomplished.",
        "Silence is a source of great strength.",
        "When you are content to be simply yourself and don't compare or compete, everyone will respect you.",
        "A good traveler has no fixed plans and is not intent on arriving.",
        "Care about what other people think and you will always be their prisoner."
    ],
    "Buddha": [
        "Peace comes from within. Do not seek it without.",
        "Three things cannot be long hidden: the sun, the moon, and the truth.",
        "The mind is everything. What you think you become.",
        "No one saves us but ourselves. No one can and no one may. We ourselves must walk the path.",
        "Holding on to anger is like grasping a hot coal with the intent of throwing it at someone else; you are the one who gets burned.",
        "All that we are is the result of what we have thought.",
        "Your purpose in life is to find your purpose and give your whole heart and soul to it."
    ],
    "Zhuangzi": [
        "Happiness is the absence of the striving for happiness.",
        "A path is made by walking on it.",
        "Flow with whatever may happen and let your mind be free.",
        "The fish trap exists because of the fish. Once you've gotten the fish you can forget the trap.",
        "Great wisdom is generous; petty wisdom is contentious.",
        "To a mind that is still, the whole universe surrenders.",
        "The perfect man has no self; the spiritual man has no achievement; the sage has no name."
    ],
    "Sun Tzu": [
        "The supreme art of war is to subdue the enemy without fighting.",
        "In the midst of chaos, there is also opportunity.",
        "If you know the enemy and know yourself, you need not fear the result of a hundred battles.",
        "Pretend inferiority and encourage his arrogance.",
        "Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt.",
        "Victorious warriors win first and then go to war, while defeated warriors go to war first and then seek to win.",
        "The greatest victory is that which requires no battle."
    ],
    "Rumi": [
        "Yesterday I was clever, so I wanted to change the world. Today I am wise, so I am changing myself.",
        "The wound is the place where the Light enters you.",
        "Silence is the language of God, all else is poor translation.",
        "Raise your words, not voice. It is rain that grows flowers, not thunder.",
        "Forget safety. Live where you fear to live. Destroy your reputation. Be notorious.",
        "You were born with wings, why prefer to crawl through life?",
        "What you seek is seeking you."
    ],
    "Rabindranath Tagore": [
        "Faith is the bird that feels the light when the dawn is still dark.",
        "You can't cross the sea merely by standing and staring at the water.",
        "The butterfly counts not months but moments, and has time enough.",
        "If you cry because the sun has gone out of your life, your tears will prevent you from seeing the stars.",
        "Let your life lightly dance on the edges of Time like dew on the tip of a leaf.",
        "The water in a vessel is sparkling; the water in the sea is dark. The small truth has words which are clear; the great truth has great silence.",
        "By plucking her petals, you do not gather the beauty of the flower."
    ],
    "Alan Watts": [
        "This is the real secret of life — to be completely engaged with what you are doing in the here and now.",
        "We seldom realize, for example, that our most private thoughts and emotions are not actually our own.",
        "The only way to make sense out of change is to plunge into it, move with it, and join the dance.",
        "The meaning of life is just to be alive. It is so plain and so obvious and so simple.",
        "Trying to define yourself is like trying to bite your own teeth.",
        "Man suffers only because he takes seriously what the gods made for fun.",
        "You are an aperture through which the universe is looking at and exploring itself."
    ],
    
    # Indian Philosophers and Saints
    "Swami Vivekananda": [
        "Arise, awake, and stop not till the goal is reached.",
        "The greatest religion is to be true to your own nature. Have faith in yourselves!",
        "All the powers in the universe are already ours. It is we who have put our hands before our eyes and cry that it is dark.",
        "Take up one idea, make that one idea your life. Think of it, dream of it, live on that idea.",
        "The fire that warms us can also consume us; it is not the fault of the fire.",
        "We are responsible for what we are, and whatever we wish ourselves to be, we have the power to make ourselves.",
        "Neither seek nor avoid, take what comes."
    ],
    "Sri Ramakrishna": [
        "Different paths lead to the same goal.",
        "As many opinions, so many paths.",
        "Knowledge leads to unity, ignorance to diversity.",
        "The winds of grace are always blowing, but you have to raise the sail.",
        "The more you go within, the more your words are backed by that silent power.",
        "When the flower blooms, the bees come uninvited.",
        "It is easy to talk on philosophy, but difficult to put it in practice."
    ],
    "Sri Aurobindo": [
        "Be conscious first of thyself within, then think and act.",
        "Life is life – whether in a cat, or dog or man. There is no difference there between a cat or a man. The idea of difference is a human conception for man's own advantage.",
        "Inspiration is a slender river of brightness leaping from a vast and eternal knowledge.",
        "The soul that can speak with its own self knows the taste of peace.",
        "The mind has to be made quiet before the psychic being can shine through it.",
        "Hidden nature is secret potential.",
        "To listen to some critics, one would imagine that only the imperfect is interesting."
    ],
    "J. Krishnamurti": [
        "The ability to observe without evaluating is the highest form of intelligence.",
        "Freedom from the desire for an answer is essential to the understanding of a problem.",
        "It is truth that liberates, not your effort to be free.",
        "The constant assertion of belief is an indication of fear.",
        "One is never afraid of the unknown; one is afraid of the known coming to an end.",
        "When you draw on memory, you are bound to repeat the past.",
        "The moment you have in your heart this extraordinary thing called love and feel the depth, the delight, the ecstasy of it, you will discover that for you the world is transformed."
    ],
    "Ramana Maharshi": [
        "Your own Self-realization is the greatest service you can render the world.",
        "Happiness is your nature. It is not wrong to desire it. What is wrong is seeking it outside when it is inside.",
        "The mind is a bundle of thoughts. The thoughts arise because there is the thinker.",
        "All that is required to realize the Self is to be still.",
        "The purpose of seeking the source of thoughts is to eliminate them.",
        "You are awareness. Awareness is another name for you.",
        "The greatest error of a man is to think that he is weak by nature, evil by nature."
    ],
    "Adi Shankaracharya": [
        "The world, like a dream full of attachments and aversions seems real until the awakening.",
        "Knowledge of the Self is not a mere intellectual knowledge. It is full experience.",
        "The mind is made up of thoughts. If you do not identify with these thoughts, you are not the mind.",
        "To be free from the thinking mind is the true ceasing of sorrow.",
        "Action is the product of the qualities inherent in nature.",
        "As one acts, so does one become.",
        "Silence is the true language of cosmic vastness."
    ],
    "Paramahansa Yogananda": [
        "Change yourself and you have done your part in changing the world.",
        "Live each moment completely and the future will take care of itself.",
        "The season of failure is the best time for sowing the seeds of success.",
        "The power of unfulfilled desires is the root of all man's slavery.",
        "If you want to be sad, no one in the world can make you happy. But if you make up your mind to be happy, no one and nothing on earth can take that happiness from you.",
        "Stillness is the altar of spirit.",
        "The happiness of one's own heart alone cannot satisfy the soul; one must try to include, as necessary to one's own happiness, the happiness of others."
    ],
    "Kabir": [
        "When I am not, then I am. When I am, then I am not.",
        "Wherever you are is the entry point.",
        "Be strong then, and enter into your own body; there you have a solid place for your feet.",
        "The river that flows in you also flows in me.",
        "I laugh when I hear that the fish in the water is thirsty.",
        "Don't go outside your house to see flowers. Inside your body there are flowers.",
        "When listening to the wise, your understanding also becomes wise."
    ],
    "Chanakya": [
        "Learn from the mistakes of others... you can't live long enough to make them all yourself.",
        "Before you start some work, always ask yourself three questions - Why am I doing it, What the results might be and Will I be successful.",
        "The biggest guru-mantra is: Never share your secrets with anybody. It will destroy you.",
        "Education is the best friend. An educated person is respected everywhere. Education beats the beauty and the youth.",
        "There is no austerity equal to a balanced mind, and there is no happiness equal to contentment.",
        "As soon as the fear approaches near, attack and destroy it.",
        "The world's biggest power is the youth and beauty of a woman."
    ],
    "Thiruvalluvar": [
        "Learning is wealth that none can destroy.",
        "It is the nature of the world that one moment someone is a stranger to you, and the next moment they are a friend.",
        "As water changes according to the soil through which it flows, so a person takes the form of the company which they keep.",
        "Virtue yields Heaven's honor and Earth's wealth.",
        "The wound that's made by fire will heal, but the wound that's made by tongue will never heal.",
        "All suffering recoils on the wrongdoer. Thus, those who inflict pain will themselves suffer pain.",
        "Like the earth that supports those who dig into it, one should sustain the malice of enemies."
    ],
    "Jaggi Vasudev (Sadhguru)": [
        "The fear is simply because you are not living with life, you are living in your mind.",
        "The most beautiful moments in life are moments when you are expressing your joy, not when you are seeking it.",
        "If you resist change, you resist life.",
        "Learning to listen is the essence of intelligent living.",
        "The significance of life is not in what you do but in how you do it.",
        "Your struggles are because you're constantly trying to fix everything around you, not yourself.",
        "The only way to experience true wellbeing is to turn inward."
    ]
}

# Map error types to philosophers who might have relevant wisdom
ERROR_PHILOSOPHER_MAP = {
    # Syntax errors
    SyntaxError: ["Wittgenstein", "Confucius", "Lao Tzu"],
    
    # Logic errors
    AssertionError: ["Aristotle", "Kant", "Plato"],
    ValueError: ["Socrates", "Camus", "Buddha"],
    TypeError: ["Marcus Aurelius", "Nietzsche", "Sun Tzu"],
    
    # Runtime errors
    RuntimeError: ["Seneca", "Epictetus", "Rumi"],
    RecursionError: ["Zhuangzi", "Sartre", "Alan Watts"],
    
    # System/IO errors
    IOError: ["Marcus Aurelius", "Rabindranath Tagore", "Confucius"],
    FileNotFoundError: ["Epictetus", "Lao Tzu", "Buddha"],
    PermissionError: ["Nietzsche", "Sun Tzu", "Kant"],
    
    # Generic errors
    Exception: ["Socrates", "Buddha", "Marcus Aurelius"],
    Warning: ["Confucius", "Seneca", "Camus"]
}

# Default philosophers for errors not explicitly mapped
DEFAULT_PHILOSOPHERS = ["Socrates", "Buddha", "Marcus Aurelius", "Lao Tzu", "Nietzsche"]

# Ensure all error types have properly associated philosophers
for error_type, philosophers in ERROR_PHILOSOPHER_MAP.items():
    for philosopher in philosophers:
        if philosopher not in PHILOSOPHER_QUOTES:
            raise ValueError(f"Philosopher '{philosopher}' referenced in ERROR_PHILOSOPHER_MAP but not in PHILOSOPHER_QUOTES")