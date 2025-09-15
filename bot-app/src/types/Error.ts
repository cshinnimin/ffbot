export class RamContentsError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "RamContentsError";
    Object.setPrototypeOf(this, RamContentsError.prototype);
  }
}

export class JsonExpectedError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "JsonExpectedError";
    Object.setPrototypeOf(this, JsonExpectedError.prototype);
  }
}