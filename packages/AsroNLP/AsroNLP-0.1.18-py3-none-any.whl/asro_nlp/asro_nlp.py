import os
import pandas as pd
import time
import swifter
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import re
import nltk
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# Create console with rich
console = Console()

class AsroNLP:
    def __init__(self):
        # Set the base directory where the 'data' folder is located
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Current directory

        # Set relative paths for all resources inside the 'data' folder
        self.stopwords_path = os.path.join(base_dir, 'data', 'stopwords.txt')
        self.normalization_path = os.path.join(base_dir, 'data', 'kamuskatabaku.xlsx')
        self.news_dictionary_path = os.path.join(base_dir, 'data', 'news_dictionary.txt')
        self.root_words_path = os.path.join(base_dir, 'data', 'kata-dasar.original.txt')
        self.additional_root_words_path = os.path.join(base_dir, 'data', 'kata-dasar.txt')
        self.lexicon_positive_path = os.path.join(base_dir, 'data', 'kamus_positive.xlsx')
        self.lexicon_negative_path = os.path.join(base_dir, 'data', 'kamus_negative.xlsx')

        # Initialize resources
        self.initialize_paths()
        self.load_resources()
        self.stemmer = StemmerFactory().create_stemmer()

    def initialize_paths(self):
        # Ensure all files exist
        self.ensure_files_exist([
            self.stopwords_path,
            self.normalization_path,
            self.news_dictionary_path,
            self.root_words_path,
            self.additional_root_words_path,
            self.lexicon_positive_path,
            self.lexicon_negative_path
        ])

    def load_resources(self):
        # Load the resources after ensuring files exist
        nltk.download('punkt', quiet=True)
        self.stopwords = self.load_stopwords()
        self.normalization_dict = self.load_excel_dict(self.normalization_path)
        self.lexicon_positive_dict = self.load_excel_dict(self.lexicon_positive_path)
        self.lexicon_negative_dict = self.load_excel_dict(self.lexicon_negative_path)
        self.news_media = self.load_news_media()
        self.root_words = self.load_root_words()

    def ensure_files_exist(self, files):
        missing_files = [file for file in files if not os.path.exists(file)]
        if missing_files:
            raise FileNotFoundError(f"Required file(s) not found: {', '.join(missing_files)}")

    def load_stopwords(self):
        with open(self.stopwords_path, "r", encoding="utf-8") as f:
            return set(f.read().splitlines())

    def load_excel_dict(self, path):
        df = pd.read_excel(path, header=None, engine='openpyxl')
        return dict(zip(df[0].astype(str).str.lower(), df[1]))

    def load_news_media(self):
        with open(self.news_dictionary_path, "r", encoding="utf-8") as f:
            return set(self.normalize_media_name(line.strip()) for line in f.readlines())

    def load_root_words(self):
        with open(self.root_words_path, 'r', encoding='utf-8') as f1, \
             open(self.additional_root_words_path, 'r', encoding='utf-8') as f2:
            return set(word.strip().lower() for word in f1).union(
                   set(word.strip().lower() for word in f2))

    @staticmethod
    def normalize_media_name(name):
        if not isinstance(name, str):
            name = str(name) if name is not None else ''
        name = re.sub(r"[^\w\d\s.]", '', name)
        name = re.sub(r"\s+", ' ', name)
        return name.lower()

    @staticmethod
    def case_folding(text):
        if not isinstance(text, str):
            text = str(text) if text is not None else ''
        return text.lower()

    @staticmethod
    def clean_text(text):
        if not isinstance(text, str):
            text = str(text) if text is not None else ''
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"\@\w+|\#", "", text)
        text = re.sub(r"\d+", "", text)
        text = re.sub(r"[^\w\s]", "", text)
        return text.strip()

    @staticmethod
    def tokenize_text(text):
        if not isinstance(text, str):
            text = str(text) if text is not None else ''
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        return [token for token in tokens if isinstance(token, str) and token not in self.stopwords and token.isalpha()]

    def normalize_text(self, tokens):
        return [self.normalization_dict.get(token, token) for token in tokens]

    def sentiment_analysis(self, tokens):
        score = 0
        positive_words = []
        negative_words = []
        for word in tokens:
            if not isinstance(word, str):
                continue
            word = word.lower()
            if word in self.lexicon_positive_dict:
                score += self.lexicon_positive_dict[word]
                positive_words.append(word)
            if word in self.lexicon_negative_dict:
                score += self.lexicon_negative_dict[word]
                negative_words.append(word)
        if score > 0:
            sentiment = 'Positive'
        elif score < 0:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        return {
            'Sentiment': sentiment,
            'Positive_Words': ', '.join(positive_words),
            'Negative_Words': ', '.join(negative_words)
        }

    def detect_source_type(self, source_identifier):
        if not isinstance(source_identifier, str):
            return 'Individual'
        normalized_identifier = self.normalize_media_name(source_identifier)
        return 'Media' if any(media_name in normalized_identifier for media_name in self.news_media) else 'Individual'

    def process_dataframe(self, df):
        text_column = 'full_text' if 'full_text' in df.columns else 'comment'
        df[text_column] = df[text_column].fillna('').astype(str)

        # Process and display token information before and after stemming
        with Progress(console=console) as progress:
            task = progress.add_task("[cyan]Processing text...", total=len(df))
            df['Case_Folded_Text'] = df[text_column].apply(self.case_folding)
            progress.update(task, advance=1)
            df['Cleaned_Text'] = df['Case_Folded_Text'].apply(self.clean_text)
            progress.update(task, advance=1)
            df = df[df['Cleaned_Text'].str.strip().ne('')].copy()
            df['Tokens'] = df['Cleaned_Text'].apply(self.tokenize_text)
            progress.update(task, advance=1)
            df['Filtered_Tokens'] = df['Tokens'].apply(self.remove_stopwords)
            progress.update(task, advance=1)
            df['Normalized_Text'] = df['Filtered_Tokens'].apply(self.normalize_text)
            progress.update(task, advance=1)
            df['Stemmed_Text'] = df['Normalized_Text'].swifter.apply(
                lambda tokens: self.stem_and_display(tokens)
            )
            progress.update(task, advance=1)
            df['Sentiment_Results'] = df['Stemmed_Text'].apply(self.sentiment_analysis)
            progress.update(task, advance=1)
            df['Sentiment'] = df['Sentiment_Results'].apply(lambda x: x['Sentiment'])
            df['Positive_Words'] = df['Sentiment_Results'].apply(lambda x: x['Positive_Words'])
            df['Negative_Words'] = df['Sentiment_Results'].apply(lambda x: x['Negative_Words'])

        channel_title_column = 'channel_title' if 'channel_title' in df.columns else 'username' if 'username' in df.columns else None
        if channel_title_column is None:
            raise ValueError("DataFrame does not contain a recognized channel title column ('channel_title' or 'username').")
        df['Source_Type'] = df.apply(lambda x: self.detect_source_type(x[channel_title_column]), axis=1)
        return df

    def stem_and_display(self, tokens):
        console.log(f"[bold yellow]Tokens before stemming: {tokens}[/bold yellow]")
        stemmed = [self.stemmer.stem(token) for token in tokens]
        console.log(f"[bold green]Tokens after stemming: {stemmed}[/bold green]")
        return stemmed

    def visualize_sentiment_and_source(self, df):
        # Sentiment Distribution
        sentiment_counts = df['Sentiment'].value_counts()
        sentiment_total = sentiment_counts.sum()
        sentiment_percentages = sentiment_counts / sentiment_total * 100

        # Display Sentiment Distribution Pie Chart
        plt.figure(figsize=(6, 6))
        plt.pie(sentiment_counts, labels=[f"{sentiment} ({count}, {percentage:.1f}%)" 
                                          for sentiment, count, percentage in zip(sentiment_counts.index, sentiment_counts, sentiment_percentages)],
                autopct='%1.1f%%', startangle=140)
        plt.title(f"Sentiment Distribution (Total: {sentiment_total} records)")
        plt.axis('equal')
        plt.show()

        # Source Type Distribution
        source_counts = df['Source_Type'].value_counts()
        source_total = source_counts.sum()
        source_percentages = source_counts / source_total * 100

        # Display Source Type Distribution Bar Chart
        plt.figure(figsize=(6, 4))
        plt.bar(source_counts.index, source_counts.values, tick_label=[f"{source} ({count}, {percentage:.1f}%)"
                                                                     for source, count, percentage in zip(source_counts.index, source_counts, source_percentages)])
        plt.title(f"Source Type Distribution (Total: {source_total} records)")
        plt.xlabel('Source Type')
        plt.ylabel('Count')
        plt.show()

    def visualize_wordcloud_and_top_words(self, df):
        sentiment_categories = ['Positive', 'Negative', 'Neutral']
        
        for sentiment in sentiment_categories:
            sentiment_text = ' '.join(
                [word for words in df[df['Sentiment'] == sentiment]['Filtered_Tokens'] for word in words]
            )
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(sentiment_text)
            
            # Display Word Cloud
            plt.figure(figsize=(10, 6))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.title(f"WordCloud for {sentiment} Sentiment")
            plt.show()

            # Top 10 Frequent Words
            sentiment_tokens = [token for tokens in df[df['Sentiment'] == sentiment]['Filtered_Tokens'] for token in tokens]
            word_counts = Counter(sentiment_tokens)
            top_10_words = word_counts.most_common(10)

            words, counts = zip(*top_10_words)
            total_words = sum(counts)
            word_percentages = [count / total_words * 100 for count in counts]

            # Display Top 10 Frequent Words with Percentages
            plt.figure(figsize=(10, 6))
            plt.bar(words, counts)
            for i, (word, count, percentage) in enumerate(zip(words, counts, word_percentages)):
                plt.text(i, count, f"{percentage:.1f}%", ha='center', va='bottom', fontsize=10)
            plt.title(f'Top 10 Frequent Words for {sentiment} Sentiment')
            plt.xlabel('Words')
            plt.ylabel('Frequency')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()

    def preprocess_and_analyze(self, input_path, output_path="output.xlsx"):
        try:
            df = pd.read_excel(input_path, engine='openpyxl')
            start_time = time.time()
            df = self.process_dataframe(df)
            df['Category'] = df.apply(lambda x: f"{x['Sentiment']} - {x['Source_Type']}", axis=1)
            end_time = time.time()

            sentiment_counts = df['Sentiment'].value_counts()
            source_type_counts = df['Source_Type'].value_counts()
            category_counts = df['Category'].value_counts()

            sentiment_table = Table(title="Sentiment Counts", title_style="bold magenta")
            sentiment_table.add_column("Sentiment", style="dim", justify="right")
            sentiment_table.add_column("Count", justify="right")
            for sentiment, count in sentiment_counts.items():
                sentiment_table.add_row(sentiment, str(count))
            console.print(sentiment_table)

            source_type_table = Table(title="Source Type Counts", title_style="bold magenta")
            source_type_table.add_column("Source Type", style="dim", justify="right")
            source_type_table.add_column("Count", justify="right")
            for source_type, count in source_type_counts.items():
                source_type_table.add_row(source_type, str(count))
            console.print(source_type_table)

            category_table = Table(title="Sentiment by Source Type", title_style="bold cyan")
            category_table.add_column("Category", style="dim", justify="right")
            category_table.add_column("Count", justify="right")
            for category, count in category_counts.items():
                category_table.add_row(category, str(count))
            console.print(category_table)

            df.to_excel(output_path, index=False, engine='openpyxl')
            console.print(f"[bold green]Processed data saved to {output_path}[/bold green]")
            console.print(f"Processing time: {end_time - start_time:.2f} seconds")

            # Visualizations
            self.visualize_sentiment_and_source(df)
            self.visualize_wordcloud_and_top_words(df)

        except Exception as e:
            console.print(f"[bold red]Error processing data: {e}[/bold red]")

