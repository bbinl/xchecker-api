// utils/cardValidator.js
const cardValidator = {
  isVisa: (cardNum) => /^4[0-9]{12}(?:[0-9]{3})?$/.test(cardNum),
  isMastercard: (cardNum) => /^5[1-5][0-9]{14}$/.test(cardNum),
  isAmex: (cardNum) => /^3[47][0-9]{13}$/.test(cardNum),
  isDiscover: (cardNum) => /^6(?:011|5[0-9]{2})[0-9]{12}$/.test(cardNum),

  luhnCheck: (cardNum) => {
    let sum = 0;
    for (let i = 0; i < cardNum.length; i++) {
      let digit = parseInt(cardNum[i]);
      if ((cardNum.length - i) % 2 === 0) {
        digit *= 2;
        if (digit > 9) digit -= 9;
      }
      sum += digit;
    }
    return sum % 10 === 0;
  },

  validate: (cardNum) => {
    const cleaned = cardNum.replace(/\D/g, '');
    if (!/^[0-9]{13,16}$/.test(cleaned)) return { valid: false };

    const cardType = cardValidator.isVisa(cleaned) ? 'VISA' :
                     cardValidator.isMastercard(cleaned) ? 'MASTERCARD' :
                     cardValidator.isAmex(cleaned) ? 'AMEX' :
                     cardValidator.isDiscover(cleaned) ? 'DISCOVER' : 'UNKNOWN';

    return {
      card_type: cardType,
      valid: cardValidator.luhnCheck(cleaned) && cardType !== 'UNKNOWN',
      message: cardValidator.luhnCheck(cleaned) ? 'Valid' : 'Invalid'
    };
  }
};

module.exports = cardValidator;
