# Split the intro into groups of 2 paragraphs each
bash split_chapter.sh chapter_intro 4

# Split the maths chapter into groups of 3
bash split_chapter.sh chapter_maths 3

# Split the taxonomy one paragraph per file (fine-grained)
bash split_chapter.sh chapter_taxonomy 1
