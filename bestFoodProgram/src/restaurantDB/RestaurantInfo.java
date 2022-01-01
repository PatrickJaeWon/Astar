package restaurantDB;

public class RestaurantInfo {
	
    private String placeName;		//가게 이름
    private String categoryName;	//카테고리 이름
    private String categoryDetail;	//카테고리 세부
    private String phone;			//연락처
    private String addressName;		//가게 주소
    private String placeBest;		//대표메뉴
    private String roadAddressName;	//도로명 주소
    private String placeUrl;
    private String id;				//PK
    private String imageUrl;
    private String mood;
    
    public RestaurantInfo(String placeName, String categoryName, String categoryDetail, String phone, String addressName, String placeBest, String roadAddressName, 
    		String placeUrl, String id, String mood, String imageUrl) {
    	this.placeName=placeName;
    	this.categoryName=categoryName;
    	this.categoryDetail=categoryDetail;
    	this.phone=phone;
    	this.addressName=addressName;
    	this.placeBest=placeBest;
    	this.roadAddressName=roadAddressName;
    	this.placeUrl=placeUrl;
    	this.id=id;
    	this.mood=mood;
    	this.imageUrl=imageUrl;
	}
    
	public String getAddressName() {
		return addressName;
	}

	public String getCategoryName() {
		return categoryName;
	}

	public String getCategoryDetail() {
		return categoryDetail;
	}

	public String getId() {
		return id;
	}

	public String getPhone() {
		return phone;
	}

	public String getPlaceName() {
		return placeName;
	}

	public String getPlaceBest() {
		return placeBest;
	}

	public String getRoadAddressName() {
		return roadAddressName;
	}

	public String getPlaceUrl() {
		return placeUrl;
	}
	
	public String getImageUrl() {
		return imageUrl;
	}

	public String getMood() {
		return mood;
	}

	public void infoShortPrint() {
		System.out.println("| " + placeName + " |");
		System.out.println("| " + categoryName + " > " + categoryDetail + " |");
		System.out.println("| 대표 메뉴 : " + placeBest + " |");
		System.out.println("-------------------------------------------------------");
		
	}
	
	public void infoFullPrint() {
		String printPlaceName=("| 매장 이름 : " + placeName);
		String printCategoryName=("| 카테고리 : " + categoryName + " > " + categoryDetail);
		String printRoadAddressName=("| 주소 : " + roadAddressName);
		String printPlaceBest=("| 대표 메뉴 : " + placeBest);
		String printPhone=("| 매장 연락처 : " + phone);
		String printPlaceUrl=("| 링크 : " + placeUrl);
	}
    
    


}
