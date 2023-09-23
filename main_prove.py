from transformers import BartForQuestionAnswering, BartTokenizer
from about_pdf import getRawTest

def main():

    # Inizializza il tokenizzatore BART
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large")

    # Inizializza il modello BART per il Question Answering
    model = BartForQuestionAnswering.from_pretrained("facebook/bart-large")

    # Carica il testo da un file TXT
    text = getRawTest()

    # Domanda da porre
    question = "Quali sono le date della sessione di laurea estiva?"

    # Tokenizza il testo e la domanda
    inputs = tokenizer.encode_plus(question, text, return_tensors="pt", padding="max_length", max_length=256, truncation=True)

    # Esegui il modello BART per il Question Answering
    start_scores, end_scores = model(**inputs)

    # Trova gli indici delle risposte iniziali e finali
    answer_start = int(start_scores.argmax())
    answer_end = int(end_scores.argmax())

    # Estrai la risposta dal testo tokenizzato
    tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end + 1])
    answer = tokenizer.convert_tokens_to_string(tokens)

    # Stampa la risposta
    print("Domanda:", question)
    print("Risposta:", answer)

if __name__ == "__name__" :
    main()