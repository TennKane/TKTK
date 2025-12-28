package com.tktk.service;

import com.tktk.interact.dto.MessageListDto;
import com.tktk.interact.dto.MessageSendDto;
import com.tktk.interact.vo.ChatListVo;
import com.tktk.interact.vo.MessageListVo;
import com.tktk.response.ResponseResult;
import org.springframework.stereotype.Service;

/**
 * 私信service
 * @author TennKane
 */
@Service
public interface PrivateMessageService {
    /**
     * 发送私信
     * @param messageSendDto 私信发送dto
     * @return ResponseResult
     */
    ResponseResult sendPrivateMessage(MessageSendDto messageSendDto);

    /**
     * 私信列表
     * @param messageListDto 私信列表dto
     * @return ResponseResult
     */
    ResponseResult<MessageListVo> privateMessageList(MessageListDto messageListDto);

    /**
     * 私信列表
     * @return ResponseResult
     */
    ResponseResult<ChatListVo> chatList();
}
