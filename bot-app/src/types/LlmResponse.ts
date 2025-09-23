// The LLM will either return a "final answer", dictated by the presence of an `answer` key,
// or it will return a request for more information, e.g.a transient response that exists
// under the hood of the bot app only, and does not get surfaced in the chat window

export type LlmResponse = {
  answerString: string;
  transientResponse: string;
};