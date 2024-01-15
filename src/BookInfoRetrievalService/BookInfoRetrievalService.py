from BookInfoRetrievalModel import BookInfo
from flask import Flask
import dotenv
import json

app = Flask(__name__)

@app.route('/health/live')
def liveness_check():
    return "OK", 200

@app.route('/health/ready')
def readiness_probe():
    return "OK", 200

@app.route('/v1/info')
def return_info_for_a_book():
    return [
        BookInfo(title='The Eye of the World', author='Robert Jordan', publisher='Tor Books', year_of_publishing=1990, description='"The Eye of the World" is the first book in Robert Jordan\'s epic fantasy series, "The Wheel of Time." Published in 1990, the novel introduces readers to a sprawling and intricately crafted world where magic, prophecy, and political intrigue shape the destinies of its diverse characters. The story begins in the quiet village of Emond\'s Field, where a young man named Rand al\'Thor discovers that he and his friends are linked to a greater destiny that involves the battle between the forces of Light and Shadow. As they embark on a perilous journey, the characters encounter mythical creatures, ancient prophecies, and powerful adversaries. Jordan\'s rich world-building, complex characters, and intricate plotlines make "The Eye of the World" a captivating and immersive entry point into the expansive Wheel of Time series, which spans fourteen books in total.').toJSON(), 
        BookInfo(title='The Great Hunt', author='Robert Jordan', publisher='Tor Books', year_of_publishing=1990, description='"The Great Hunt" is the second book in Robert Jordan\'s epic fantasy series, "The Wheel of Time." Published in 1991, the novel continues the expansive and intricate tale set in a world where a cosmic struggle between good and evil unfolds. The story picks up with Rand al\'Thor, the protagonist, who is drawn deeper into his role as the Dragon Reborn, a prophesied figure destined to confront the Dark One and reshape the fate of the world. As the characters navigate political alliances, ancient prophecies, and magical challenges, they embark on a quest to retrieve the Horn of Valere and the legendary artifact known as the Great Horn. The book is marked by Jordan\'s signature world-building, intricate plot twists, and the deepening complexity of characters who face both internal and external challenges. "The Great Hunt" continues to build upon the rich tapestry of "The Wheel of Time" series, offering readers a compelling blend of adventure, magic, and political intrigue.').toJSON(), 
        BookInfo(title='The Way of Kings', author='Brandon Sanderson', publisher='Tor Books', year_of_publishing=2010, description='"The Way of Kings" is the first installment in Brandon Sanderson\'s highly acclaimed epic fantasy series, "The Stormlight Archive." Published in 2010, the novel introduces readers to the sprawling world of Roshar, a land constantly battered by magical storms. The story revolves around multiple protagonists, each grappling with their own challenges and mysteries. At the heart of the narrative is the character Kaladin, a former soldier turned slave, who becomes entwined in a larger struggle for power, justice, and the survival of the world. The novel is renowned for its intricate world-building, innovative magic system based on the use of magical gemstones, and Sanderson\'s trademark ability to weave complex plots. "The Way of Kings" sets the stage for an epic tale of political intrigue, war, and the search for ancient, world-altering knowledge, captivating readers with its depth and intricacy.').toJSON(),
        BookInfo(title='The Words of Radience', author='Brandon Sanderson', publisher='Tor Books', year_of_publishing=2014, description='"Words of Radiance" is the second book in Brandon Sanderson\'s captivating fantasy series, "The Stormlight Archive." Published in 2014, the novel continues the epic saga set in the world of Roshar. The narrative follows multiple characters, each with their own compelling storylines, as they navigate a world rife with magical storms, political intrigue, and cosmic conflict. At its core is the character Kaladin Stormblessed, who strives to protect and lead despite facing numerous challenges. The plot delves into the mysteries of the Knights Radiant, an ancient order with magical abilities fueled by powerful gemstones. As the characters discover more about the secrets of Roshar and its enigmatic history, they become entangled in a struggle for power, truth, and the survival of their world. Known for his meticulous world-building, intricate plots, and unique magic systems, Sanderson weaves a tapestry of suspense and discovery in "Words of Radiance." The novel captivates readers with its rich character development, dynamic action sequences, and the promise of uncovering deeper layers of the expansive narrative, making it a worthy continuation of "The Stormlight Archive" series.').toJSON(),
    ]


if __name__ == '__main__':
    config = dotenv.dotenv_values(".env")

    app.run(port=5000, host="0.0.0.0")
