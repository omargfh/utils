function download(serializable: object, name?: string) {
  try {
    const serliazed = JSON.stringify(serializable);
    const blob = new Blob([serliazed]);
    const href = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.download = name ?? "file.json";
    a.href = href;
    a.click();
  } catch (e) {
    console.warn(e);
  }
}

interface GenContentConfig {
  averageWordLength?: number;
  paragraphLengthInWords?: number;
  sentenceLengthInWords?: number;
}
function generateContent(
  source: string,
  paragraphs?: number,
  config?: GenContentConfig
): string[] {
  if (!paragraphs) {
    paragraphs = 10;
  }

  const dictionary = source.split(" ")
    .map((e) => e.replace(/[^\w]/, ""))
    .map((e) => e.toLowerCase());
  const randomWord = () =>
    dictionary[Math.floor(Math.random() * dictionary.length)];

  // Heuristics
  const wordLength = config?.averageWordLength || 6;
  const paragaphTargetLength =
    config?.paragraphLengthInWords || 250 * wordLength;
  const sentenceTargetLength = config?.sentenceLengthInWords || 5 * wordLength;
  function stochasticLargerThanOrEq(props: {
    arg1: number;
    arg2: number;
    limit?: number;
    probabilityOfSuccess: number /* 0.0 - 1.0 */;
  }) {
    if (props.limit && props.arg1 >= props.limit) {
      return true;
    }
    const randomValue = Math.random();
    if (randomValue <= props.probabilityOfSuccess) {
      if (props.arg1 >= props.arg2) {
        return true;
      }
    }
    return false;
  }

  const paragraphsContent: string[] = [];
  for (let i = 0; i < paragraphs; i++) {
    const paragraphContent: string[] = [];
    while (
      !stochasticLargerThanOrEq({
        arg1: paragraphContent.join(" ").length,
        arg2: paragaphTargetLength,
        limit: paragaphTargetLength * 1.1,
        probabilityOfSuccess: 0.3
      })
    ) {
      const sentencesContent: string[] = [];
      while (
        !stochasticLargerThanOrEq({
          arg1: sentencesContent.join(" ").length,
          arg2: sentenceTargetLength,
          limit: sentenceTargetLength * 10,
          probabilityOfSuccess: 0.1
        })
      ) {
        const word = randomWord();
        if (sentencesContent.length === 0) {
          sentencesContent.push(word[0].toUpperCase() + word.slice(1));
        } else {
          sentencesContent.push(word);
        }
      }
      paragraphContent.push(sentencesContent.join(" ") + ".");
    }
    paragraphsContent.push(paragraphContent.join(" "));
  }
  return paragraphsContent;
}
