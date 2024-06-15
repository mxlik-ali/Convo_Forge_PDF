import re
import html

def clean_references1(documents: list) -> str:
    """
    Clean and format references from retrieved documents.

    Parameters:
        documents (List): List of retrieved documents.

    Returns:
        str: A string containing cleaned and formatted references.
    """
    documents = [str(x) + "\n\n" for x in documents]
    markdown_documents = ""
    counter = 1

    for doc in documents:
        # print(doc)
        # Extract content using regex
        match = re.search(r"page_content='\[\"(.*?)\"\]'", doc, re.DOTALL)
        # print(match)
        if match:
            content = match.group(1)
            
            # Ensure content is a string before processing
            if isinstance(content, str):
                # Decode newlines and other escape sequences
                content = bytes(content, "utf-8").decode("unicode_escape")

                # Replace escaped newlines with actual newlines
                content = re.sub(r'\\n', '\n', content)
                
                # print(content)
                # Remove special tokens
                content = re.sub(r'\s*<EOS>\s*<pad>\s*', ' ', content)
                # Remove any remaining multiple spaces
                content = re.sub(r'\s+', ' ', content).strip()

                # Decode HTML entities
                content = html.unescape(content)
                # Replace incorrect unicode characters with correct ones
                content = content.encode('latin1').decode('utf-8', 'ignore')

                # Replace incorrect unicode characters with correct ones
                replacements = {
                    'â': '-', 'â': '∈', 'Ã': '×', 'ï¬': 'fi', 
                    'Â·': '·', 'ï¬': 'fl'
                }
                for old, new in replacements.items():
                    content = re.sub(old, new, content)

                # Append cleaned content to the markdown string
                markdown_documents += f"# Retrieved content {counter}:\n" + content + "\n\n"
            else:
                markdown_documents += f"# Retrieved content {counter}:\n" + "Content is not a string\n\n"
        else:
            markdown_documents += f"# Retrieved content {counter}:\n" + "No match found\n\n"
        counter += 1
    # print(markdown_documents)
    return markdown_documents


# # Example usage with the provided input format:
# document_list = ["""Document(page_content='["\\n\\nAmarok the lone wolf\\n\\nIn the shadowed embrace of the Alaskan mountains, where the snow blankets the earth in a pristine white and the northern lights dance across the sky like ethereal spirits, there lived a lone wolf named Amarok. His coat was a tapestry of silver and midnight, a reflection of the landscape he called home. Amarok was a creature of solitude, but his heart ached with the memory of the family he had lost to the unforgiving wilderness.\\n\\nAmarok\'s journey began on a day when the sky wept snowflakes as large as feathers, and the wind whispered secrets only the mountains could understand. He had been separated from his pack during a fierce winter storm that had descended upon them like a ravenous beast. The pack had been everything to Amarok: his community, his support, his family. Now, he roamed the vast expanse of the Alaskan range, driven by a deep longing to find them.\\n\\nEach day was a testament to his resilience. Amarok traversed steep cliffs that clawed at the sky, crossed frozen rivers that mirrored the heavens, and navigated dense forests that stood as silent sentinels. His keen senses were his guide; his howl, a song of both sorrow and hope, echoed through the valleys, a call to the family he yearned to see once more.\\n\\nAs the seasons turned, Amarok\'s search led him to the heart of the mountains, where the air was thin and the stars seemed close enough to touch. It was here, in the realm of the eagles, that Amarok found a clue. A familiar scent carried on the breeze, a scent that quickened his pulse and filled his being with a mixture of excitement and trepidation. It was the unmistakable scent of his pack.\\n\\nWith renewed vigor, Amarok followed the trail, his paws barely touching the snow as he raced against time. The scent grew stronger, guiding him over a ridge that revealed a valley cradled by the mountains. And there, in the distance, he saw them: his family, alive and thriving. They were playing, their bodies a blur of motion against the stark landscape, their joyful yips reaching Amarok\'s ears like a melody long forgotten.\\n\\nAmarok approached cautiously, his heart pounding with a mixture of joy and uncertainty. Would they remember him? Would they accept him back into the fold? As he neared, the pack caught sight of him. For a moment, time stood still, the only movement the gentle fall of snowflakes between them.\\n\\nThen, recognition sparked in their eyes, and one by one, they came forward. Nuzzles and licks were exchanged, each touch a word in the silent language of wolves. Amarok was home. The pack was whole once more, and together, they raised their voices to the sky, a chorus of unity and belonging that resonated through the mountains of Alaska.\\n\\nAmarok, the lone wolf who had braved the wilderness in search of his family, had found more than he had ever hoped for. He had found his way back to love, to connection, to the place where his spirit ran free. And there, amidst the peaks that touched the heavens, he knew he would never be alone again.\\n\\n\\n\\nFred the red fish\\n\\nOnce upon a time, in the vast, shimmering ocean, there lived a small red fish named Fred. Fred was not just any ordinary fish; his scales sparkled like rubies under the sun\'s caress, and his eyes gleamed with the curiosity of a thousand adventures yet to come. He lived happily in a cozy coral reef, bustling with marine life, alongside his loving family.\\n\\nFred\'s family was known for their bravery and kindness. His mother, Coraline, was wise and nurturing, always ready with a story or a comforting fin. His father, Marlin, was a strong and daring explorer who regaled Fred and his siblings with tales of his travels through underwater canyons and past shipwrecks.\\n\\nAs Fred grew, so did his desire for adventure. He was eager to explore every nook and cranny of the reef, and his parents often found him chasing after tiny shrimp or playing hide-and-seek with the seahorses. Fred\'s best friend was a playful dolphin named Delphi, who shared his love for exploration and often joined him on his escapades.\\n\\nOne day, while Fred and Delphi were exploring the edge of their reef, they stumbled upon a strange object that had sunk to the ocean floor. It was a bottle with a piece of parchment inside. Fred, with his nimble fins, managed to coax the parchment out. It was a map, one that pointed to a hidden treasure located in a distant part of the ocean, beyond the familiar waters of their home.\\n\\nThe promise of adventure was too great to resist. Fred kissed his family goodbye, promising to return with stories to rival his father\'s. With Delphi by his side, Fred set off on the greatest adventure of his life.\\n\\nTheir journey was filled with wonders and dangers alike. They swam through forests of kelp that towered like skyscrapers, and evaded the grasp of a hungry octopus with quick thinking and quicker swimming. They met wise old turtles who spoke of the currents that could carry them swiftly to their destination and encountered schools of fish that shimmered like living rainbows.\\n\\nAs they ventured into the open ocean, a storm brewed above, sending powerful waves that churned the water into a frothy turmoil. Fred and Delphi dove deep to escape the tumult, finding solace in the quiet depths. It was there, in the serene darkness, that they discovered a glowing garden of bioluminescent jellyfish, a sight so beautiful it took their breath away.\\n\\nFinally, after what seemed like an eternity of swimming, they reached the location marked on the map. It was a sunken pirate ship, its timbers worn by time and teeming with sea life. Fred and Delphi searched through the wreckage and found the treasure chest, just as the map had promised. It was filled with glittering jewels and gold, but to Fred, the real treasure was the journey he had undertaken and the memories he had created with his friend.\\n\\nTriumphant, Fred and Delphi made their way back home, where they were greeted with cheers and open fins. Fred\'s family listened in awe as he recounted his adventure, his eyes shining with the reflection of the deep sea and the treasures it held.\\n\\nFred had grown in more ways than one. He had faced challenges and had come to understand that the ocean was vast and full of mysteries, some perilous, but all enchanting. He realized that home was not just a place but the love that awaited him there. And so, Fred the small red fish lived happily ever after, his heart as deep and wide as the ocean he called home, always ready for the next great adventure.\\n\\n\\n\\nLily the bee\\n\\nOnce upon a time in the lush, vibrant meadows of Blossom Valley, there lived a young bee named Lily. She was smaller than the other bees, but what she lacked in size, she made up for with her boundless love for flowers and her family. Lily spent her days flitting from bloom to bloom, her wings shimmering in the sunlight as she collected nectar for"]')"""]

# # Call the function and print the cleaned text
# cleaned_text = clean_references1(document_list)
# print(cleaned_text)


