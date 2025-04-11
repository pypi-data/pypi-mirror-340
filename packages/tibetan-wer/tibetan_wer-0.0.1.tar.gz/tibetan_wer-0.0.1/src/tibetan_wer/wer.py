import botok
import numpy as np

tokenizer = botok.WordTokenizer()

def word_segment(sentence, tokenizer=tokenizer):
    """
    Segment a sentence into words using a custom tokenizer.

    Parameters
    ----------
    sentence : str
        The input sentence to be segmented.
    tokenizer : callable, optional
        A tokenizer function or object with a `.tokenize()` method.
        Default is the globally defined `tokenizer`.

    Returns
    -------
    list of str
        A list of cleaned word strings extracted from the input sentence.
    """

    tokens = tokenizer.tokenize(sentence.strip())
    
    words = [elt['text_cleaned'] for elt in tokens]

    return words

def wer(prediction, reference):
    """
    Compute Word Error Rate (WER) between a predicted and reference transcription.

    Parameters
    ----------
    prediction : str
        Predicted words from the ASR model.
    reference : str
        Ground truth words.

    Returns
    -------
    float
        Word Error Rate (WER)
    """

    prediction = word_segment(prediction)
    reference = word_segment(reference)

    p_len = len(prediction)
    r_len = len(reference)

    # Initialize DP matrix
    d = np.zeros((r_len + 1, p_len + 1), dtype=np.int32)
    for i in range(r_len + 1):
        d[i][0] = i
    for j in range(p_len + 1):
        d[0][j] = j

    # Fill DP matrix
    for i in range(1, r_len + 1):
        for j in range(1, p_len + 1):
            if reference[i - 1] == prediction[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(
                    d[i - 1][j] + 1,    # deletion
                    d[i][j - 1] + 1,    # insertion
                    d[i - 1][j - 1] + 1 # substitution
                )

    return d[r_len][p_len] / r_len if r_len > 0 else float('inf')
