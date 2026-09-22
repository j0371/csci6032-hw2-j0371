Author: Marcus Higgins</br>
Assignment: Homework 2</br>
Course: CSCI 6032</br>
Institution: The University of Mississippi</br>
Remote Repo Loctation: https://github.com/j0371/csci6032-hw2-j0371.git</br>
Operating System: Windows 11</br>

This repository hosts my submission for The second homework assignment for CSCI 6032 - Machine Learning during the fall semester of 2026 at The University of Mississppi. When this project is complete, it will serve as a showcase to demonstrate various ways of interacting and utilizing with the agentic and automation capabilities of Large Language Models in a safe and secure way using Github Copilot. This includes utilizing agents, git, docker, and skills.

Usage:
Run the text statistics utility with a UTF-8 text file as the single argument:
python src/text_stats.py sample.txt

The script prints JSON in the format:
{"lines": 5, "words": 55, "characters": 281}

Optionally, include --top N to report the N most frequent words, case-insensitively, with deterministic tie-breaking by alphabetical word order:
python src/text_stats.py --top 3 sample.txt

Example output:
{"lines": 5, "words": 55, "characters": 281, "top_words": [["i", 4], ["the", 3], ["am", 2]]}

This counts newline-separated lines, whitespace-delimited words, and total characters in the file. The word-frequency ranking ignores case and keeps a stable order when counts tie.
