package com.tktk.video.vo;

import lombok.Data;

/**
 * @author TennKane
 */
@Data
public class VideoUploadVo {
    /**
     * 视频名称
     */
    private String videoUrl;

    /**
     * 视频封面
     */
    private String coverUrl;
}
