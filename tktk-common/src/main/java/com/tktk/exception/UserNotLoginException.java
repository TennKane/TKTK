package com.tktk.exception;

import com.tktk.constant.ResponseConstant;

/**
 * 用户未登录异常
 * @author TennKane
 */
public class UserNotLoginException extends CustomException {
    public UserNotLoginException() {
        super(ResponseConstant.NEED_LOGIN);
    }
}
