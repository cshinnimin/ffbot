export class BestiaryRequestInvalidFormatError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "BestiaryRequestInvalidFormatError";
    Object.setPrototypeOf(this, BestiaryRequestInvalidFormatError.prototype);
  }
}
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

export class FlaskRamWriteError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "FlaskRamWriteError";
    Object.setPrototypeOf(this, FlaskRamWriteError.prototype);
  }
}

export class FinalMessageContainsRamAddressesError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "FinalMessageContainsRamAddressesError";
    Object.setPrototypeOf(this, FinalMessageContainsRamAddressesError.prototype);
  }
}

export class FinalMessageContainsSquareBracketsError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "FinalMessageContainsSquareBracketsError";
    Object.setPrototypeOf(this, FinalMessageContainsSquareBracketsError.prototype);
  }
}