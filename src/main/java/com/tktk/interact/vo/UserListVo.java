package com.tktk.interact.vo;

import com.tktk.user.vo.UserPersonalInfoVo;
import lombok.Builder;
import lombok.Data;

import java.util.List;

/**
 * 用户列表Vo
 * @author TennKane
 */
@Data
@Builder
public class UserListVo {

    /**
     * 总数
     */
    private Integer total;

    /**
     * 用户列表
     */
    private List<UserPersonalInfoVo> list;

}
