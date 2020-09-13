from utils.mysql_tool import DbBase, db
from sqlalchemy.orm import aliased


class PMSProductCategory(DbBase):
    """
    商品分类表
    """
    __tablename__ = 'pms_product_category'
    parent_id = db.Column(db.BigInteger)  # 上级分类的编号，0代表一级分类
    name = db.Column(db.VARCHAR(64))  # 名称
    level = db.Column(db.Integer)  # 分类级别 0：一级 1：二级
    product_count = db.Column(db.Integer)  # 商品数量
    product_unit = db.Column(db.VARCHAR(64))  # 商品单位
    nav_status = db.Column(db.Integer)  # 是否显示在导航栏 0：不显示 1：显示
    show_status = db.Column(db.Integer)  # 显示状态 0：不显示 1：显示
    sort = db.Column(db.Integer)  # 排序
    icon = db.Column(db.VARCHAR(255))  # 图标
    keywords = db.Column(db.VARCHAR(255))  # 关键字
    description = db.Column(db.Text)  # 描述


class PMSBrand(DbBase):
    """
    商品品牌表
    """
    __tablename__ = 'pms_brand'
    name = db.Column(db.VARCHAR(64))  # 名称
    first_letter = db.Column(db.VARCHAR(8))  # 首字母
    sort = db.Column(db.Integer)  # 排序
    factory_status = db.Column(db.Integer)  # 是否品牌制造商 0：不是 1：是
    show_status = db.Column(db.Integer)  # 显示状态 0：不显示 1：显示
    product_count = db.Column(db.Integer)  # 产品数量
    product_comment_count = db.Column(db.Integer)  # 产品评论数量
    logo = db.Column(db.VARCHAR(255))  # 品牌logo
    big_pic = db.Column(db.VARCHAR(255))  # 关键字
    brand_story = db.Column(db.Text)  # 描述


class PMSProductAttributeCategory(DbBase):
    """
    商品属性分类表，商品的规格用户参数，规格用于用户购买时选择，参数用于标示商品属性以及搜索时筛选
    """
    __tablename__ = 'pms_product_attribute_category'
    name = db.Column(db.VARCHAR(64))  # 名称
    attribute_count = db.Column(db.Integer)  # 属性数量
    param_count = db.Column(db.Integer)  # 参数数量


class PMSProductAttribute(DbBase):
    """
    商品属性表，type 字段用于控制其是规格还是参数
    """
    __tablename__ = 'pms_product_attribute'
    product_attribute_category_id = db.Column(db.BigInteger)  # 商品属性分类id
    name = db.Column(db.VARCHAR(64))  # 名称
    select_type = db.Column(db.Integer)  # 属性选择类型：0->唯一；1->单选；2->多选；对应属性和参数意义不同
    input_type = db.Column(db.Integer)  # 参数数量
    input_list = db.Column(db.VARCHAR(255))  # 参数数量
    sort = db.Column(db.Integer)  # 排序字段：最高的可上传图片
    filter_type = db.Column(db.Integer)  # 分类筛选样式 1：普通 2：颜色
    search_type = db.Column(db.Integer)  # 检索类型 0：不需要检索 1：关键字检索 2：范围检索
    related_status = db.Column(db.Integer)  # 相同属性产品是否关联 0：不关联 1：关联
    hand_add_status = db.Column(db.Integer)  # 是否支持手动新增 0：不支持 1：支持
    type = db.Column(db.Integer)  # 属性类型 0：规格 1：参数


class PMSProductAttributeValue(DbBase):
    """
    商品属性值表，
    如果对应的参数是规格且规格支持手动添加，那么该表用于存储手动新增的值；
    如果对应的商品属性是参数，那么该表用于存储参数的值。
    """
    __tablename__ = 'pms_product_attribute_value'
    product_id = db.Column(db.BigInteger)  # 商品id
    product_attribute_id = db.Column(db.BigInteger)  # 商品属性id
    value = db.Column(db.VARCHAR(64))  # 手动添加规格或参数的值，参数单值，规格有多个时以逗号隔开


class PMSProductCategoryAttributeValueRelation(DbBase):
    """
    商品分类和属性关系表，用于选中分类后搜索时生成筛选属性
    """
    __tablename__ = 'pms_product_category_attribute_relation'
    product_category_id = db.Column(db.BigInteger)  # 商品分类id
    product_attribute_id = db.Column(db.BigInteger)  # 商品属性id


class PMSProduct(DbBase):
    """
    商品表，包括的信息： 1.商品基本信息； 2.商品促销信息； 3.商品属性信息； 4.商品的关联；
    """
    __tablename__ = 'pms_product'
    brand_id = db.Column(db.BigInteger)  # 品牌 id
    product_category_id = db.Column(db.BigInteger)  # 品牌分类 id
    feight_template_id = db.Column(db.BigInteger)  # 运费模板 id
    product_attribute_category_id = db.Column(db.BigInteger)  # 品牌属性分类 id
    name = db.Column(db.VARCHAR(64), nullable=False)  # 商品名称
    pic = db.Column(db.VARCHAR(255))  # 商品图片
    product_sn = db.Column(db.VARCHAR(64), nullable=False)  # 货号
    delete_status = db.Column(db.Integer)  # 删除状态
    publish_status = db.Column(db.Integer)  # 上架状态
    new_status = db.Column(db.Integer)  # 新品状态
    recommand_status = db.Column(db.Integer)  # 推荐状态
    verify_status = db.Column(db.Integer)  # 审核状态
    sort = db.Column(db.Integer)  # 排序
    sale = db.Column(db.Integer)  # 销量

    price = db.Column(db.DECIMAL(10, 2))  # 价格
    promotion_price = db.Column(db.DECIMAL(10, 2))  # 促销价格

    gift_growth = db.Column(db.Integer, default=0)  # 赠送的成长值
    gift_point = db.Column(db.Integer, default=0)  # 赠送的积分
    use_point_limit = db.Column(db.Integer)  # 限制使用的积分数
    sub_title = db.Column(db.VARCHAR(255))  # 副标题
    description = db.Column(db.Text)  # 商品描述

    original_price = db.Column(db.DECIMAL(10, 2))  # 市场价

    stock = db.Column(db.Integer)  # 库存
    low_stock = db.Column(db.Integer)  # 库存预警值
    unit = db.Column(db.VARCHAR(16))  # 单位

    weight = db.Column(db.DECIMAL(10, 2))  # 商品重量，默认为克

    preview_status = db.Column(db.Integer)  # 是否为预告商品 0：不是 1：是
    service_ids = db.Column(db.VARCHAR(64))  # 以逗号分割的产品服务； 1：退还无忧 2：快速退款 3：免费包邮
    keywords = db.Column(db.VARCHAR(255))  # 关键字
    note = db.Column(db.VARCHAR(255))  # 备注
    album_pics = db.Column(db.VARCHAR(255))  # 画册图片，
    detail_title = db.Column(db.VARCHAR(255))  # 详情标题
    detail_desc = db.Column(db.Text)  # 详情描述
    detail_html = db.Column(db.Text)  # 产品详情网页内容
    detail_mobile_html = db.Column(db.Text)  # 移动端网页内容
    promotion_start_time = db.Column(db.DateTime)  # 促销开始时间
    promotion_end_time = db.Column(db.DateTime)  # 促销结束时间
    promotion_per_limit = db.Column(db.Integer)  # 活动限购数量
    promotion_type = db.Column(db.Integer)  # 促销类型 0：没有促销使用原价 1：使用促销价 2：使用会员价 3：使用阶梯价格 4：使用满减价格 5：限时价
    product_category_name = db.Column(db.VARCHAR(255))  # 产品分类名称
    brand_name = db.Column(db.VARCHAR(255))  # 品牌名称

    def serialize(self):
        pass


class PMSSKUStock(DbBase):
    """SKU(Stock keeping unit) 库存量单位，SPU(Standard product unit) 标准产品单位"""
    __tablename__ = 'pms_sku_stock'
    product_id = db.Column(db.BigInteger)  # 商品 id
    sku_code = db.Column(db.VARCHAR(64), nullable=False)  # sku编码
    price = db.Column(db.DECIMAL(10, 2))  # 价格
    stock = db.Column(db.Integer, default=0)  # 库存
    low_stock = db.Column(db.Integer)  # 预警库存
    sp1 = db.Column(db.VARCHAR(64))  # 规格属性1
    sp2 = db.Column(db.VARCHAR(64))  # 规格属性2
    sp3 = db.Column(db.VARCHAR(64))  # 规格属性3
    pic = db.Column(db.VARCHAR(255))  # 展示图片
    sale = db.Column(db.Integer, default=0)  # 销量
    promotion_price = db.Column(db.DECIMAL(10, 2))  # 促销价格
    lock_stock = db.Column(db.Integer, default=0)  # 锁定库存


class PMSProductLadder(DbBase):
    """商品阶梯价格表，商品优惠相关表，购买同商品满足一定数量后，可以使用打折价格进行购买，如 满两件八折"""
    __tablename__ = 'pms_product_ladder'
    product_id = db.Column(db.BigInteger)  # 商品 id
    count = db.Column(db.Integer)  # 满足的商品数量
    discount = db.Column(db.DECIMAL(10, 2))  # 折扣
    price = db.Column(db.DECIMAL(10, 2))  # 折后价格


class PMSProductFullReduction(DbBase):
    """商品满减表，购买同商品满一定金额后，可以减免一定金额，如买200-15"""
    __tablename__ = 'pms_product_full_reduction'
    product_id = db.Column(db.BigInteger)  # 商品 id
    full_price = db.Column(db.DECIMAL(10, 2))  # 满足金额
    reduce_price = db.Column(db.DECIMAL(10, 2))  # 减少金额


class PMSMemberPrice(DbBase):
    """会员价格表，根据不同等级的会员可以以不同的价格购买"""
    __tablename__ = 'pms_member_price'
    product_id = db.Column(db.BigInteger)  # 商品 id
    member_level_id = db.Column(db.BigInteger)  # 会员价格
    member_price = db.Column(db.DECIMAL(10, 2))  # 会员价格
    member_level_name = db.Column(db.VARCHAR(100))  # 会员等级名称


"""  =====商品评价与回复=====  """


class PMSComment(DbBase):
    """商品评价表"""
    __tablename__ = 'pms_comment'
    product_id = db.Column(db.BigInteger)  # 商品 id
    member_nick_name = db.Column(db.VARCHAR(255))  # 会员昵称
    product_name = db.Column(db.VARCHAR(255))  # 商品名称
    star = db.Column(db.Integer)  # 评价星级 0~5
    member_ip = db.Column(db.VARCHAR(64))  # 评价的ip地址
    create_time = db.Column(db.DateTime)
    show_status = db.Column(db.Integer)  # 评价星级 0~5
    product_attribute = db.Column(db.VARCHAR(255))  # 商品名称
    collection_count = db.Column(db.Integer)  # 评价星级 0~5
    read_count = db.Column(db.Integer)  # 评价星级 0~5
    content = db.Column(db.Integer)  # 评价星级 0~5
    pics = db.Column(db.Integer)  # 评价星级 0~5
    member_icon = db.Column(db.Integer)  # 评价星级 0~5
    replay_count = db.Column(db.Integer)  # 评价星级 0~5


p = aliased(PMSProduct)
pav = aliased(PMSProductAttributeValue)
pa = aliased(PMSProductAttribute)
