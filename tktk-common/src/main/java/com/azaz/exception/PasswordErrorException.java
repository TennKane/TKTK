package com.tktk.exception;

import com.tktk.constant.ResponseConstant;

/**
 * @author TennKane
 */
public class PasswordErrorException extends CustomException{

        public PasswordErrorException() {
            super(ResponseConstant.PASSWORD_ERROR);
        }

        public PasswordErrorException(String msg) {
            super(msg);
        }
}
