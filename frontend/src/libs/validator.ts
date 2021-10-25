import { ValidateParam, ValidateData, Validator } from '@/libs/interface'

export const emailValidator = (param: ValidateParam): ValidateData => {
  const key = param.key
  if (!/^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(param.value)) {
    return {
      key,
      type: 'invalidEmail',
      status: false,
      message: '이메일 형식이 올바르지 않습니다. 다시 입력해주세요.',
    }
  }
  return {
    key,
    type: 'invalidEmail',
    status: true,
  }
}

export const passwordSecurityValidator = (
  param: ValidateParam
): ValidateData => {
  const key = param.key
  if (
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/.test(
      param.value
    )
  ) {
    return {
      key,
      type: 'weekPassword',
      status: true,
    }
  }
  return {
    key,
    type: 'weekPassword',
    status: false,
    message: '총 8자 이상, 영문자/숫자/특수문자 조합을 입력해주세요.',
  }
}

export const passwordConfirmValidator = (
  param: ValidateParam,
  password: string | undefined
): ValidateData => {
  const key = param.key
  if (password !== param.value) {
    return {
      key,
      type: 'passwordConfirmFailed',
      status: false,
      message: '비밀번호가 일치하지 않습니다.',
    }
  }
  return {
    key,
    type: 'passwordConfirmFailed',
    status: true,
  }
}

export const phoneNumberValidator = (param: ValidateParam): ValidateData => {
  const key = param.key
  return {
    key,
    type: 'invalidPhoneNumber',
    status: true,
  }
}

// 1. 필수 입력
export const requiredValidator: Validator = (key, value) => {
  if (!value) {
    return {
      key,
      type: 'required',
      status: false,
      message: '필수 입력입니다',
    }
  }
  return {
    key,
    type: 'required',
    status: true,
  }
}

export const simpleEmailValidator: Validator = (key, value) => {
  const regex = /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/
  if (!regex.test(String(value))) {
    return {
      key,
      type: 'invalidEmail',
      status: false,
      message: '이메일 형식이 유효하지 않습니다',
    }
  }
  return {
    key,
    type: 'invalidEmail',
    status: true,
  }
}
