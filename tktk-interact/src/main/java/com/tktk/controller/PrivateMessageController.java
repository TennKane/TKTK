package com.tktk.controller;

import com.tktk.interact.dto.MessageListDto;
import com.tktk.interact.dto.MessageSendDto;
import com.tktk.interact.vo.ChatListVo;
import com.tktk.interact.vo.MessageListVo;
import com.tktk.response.ResponseResult;
import com.tktk.service.PrivateMessageService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

/**
 * 私信控制器
 * @author TennKane
 */
@RestController
@RequestMapping("/tktk/interact/message")
public class PrivateMessageController {
    @Resource
    private PrivateMessageService privateMessageService;

    /**
     * 发送私信
     * @param messageSendDto 私信发送dto
     * @return ResponseResult
     */
    @PostMapping("/send")
    public ResponseResult sendPrivateMessage(MessageSendDto messageSendDto) {
        return privateMessageService.sendPrivateMessage(messageSendDto);
    }

    /**
     * 私信列表
     * @param messageListDto 私信列表dto
     * @return  ResponseResult
     */
    @GetMapping("/list")
    public ResponseResult<MessageListVo> privateMessageList(MessageListDto messageListDto) {
        return privateMessageService.privateMessageList(messageListDto);
    }

    /**
     * 私信列表
     * @return  ResponseResult
     */
    @GetMapping("/chatList")
    public ResponseResult<ChatListVo> chatList() {
        return privateMessageService.chatList();
    }
}
