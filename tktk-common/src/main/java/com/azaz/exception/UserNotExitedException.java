package com.tktk.exception;

import com.tktk.constant.ResponseConstant;

/**
 * @author TennKane
 */
public class UserNotExitedException extends CustomException {

    public UserNotExitedException() {
        super(ResponseConstant.USER_NOT_EXIST);
    }

    public UserNotExitedException(String message) {
        super(message);
    }
}
