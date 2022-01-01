package frame;

import static frame.Constant.CATEGORY_NAME_BASIC;
import static frame.Constant.PLACE_BEST_BASIC;
import static frame.Constant.PLACE_NAME_BASIC;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JPanel;
import javax.swing.SwingConstants;

import restaurantDB.RestaurantList;


public class FrameCategoryChioce extends JPanel {
	
	private static String ShortPrintPlaceName;
	private static String ShortPrintCategory;
	private static String ShortPrintPlaceBest;
	
	
	//private static ArrayList<JButton> restaurantChioce;
	int height = 50;
	
	public FrameCategoryChioce(RestaurantList restaurantList, String categoryName, String mood, int forCount, int forNum) {
		setBackground(new Color(255, 192, 203));
		setLayout(null);
		setSize(400, 700);
		int pageView = 0;
		int count = forCount;
		forCount = 0;
		
		
		for(int i=forNum;i<restaurantList.Info().size();i++) {
			forCount++;
			if(restaurantList.Info().get(i).getMood().equals(mood)) {
				if(categoryName.equals("ALL")) {
					makeButton(restaurantList, i, categoryName, mood);
					pageView++;

				}
				else if(restaurantList.Info().get(i).getCategoryName().equals(categoryName)) {
					makeButton(restaurantList, i, categoryName, mood);
					pageView++;
				}
				
			}
			else if(mood.equals("선택안함")) {
				if(categoryName.equals("ALL")) {
					makeButton(restaurantList, i, categoryName, mood);
					pageView++;

				}
				else if(restaurantList.Info().get(i).getCategoryName().equals(categoryName)) {
					makeButton(restaurantList, i, categoryName, mood);
					pageView++;
				}
				
			}
			
			
			
			if(pageView == 8) {
				break;
			}
			
		}
		
		if(pageView == 8 && (forNum + forCount) < restaurantList.Info().size()) {
			int k = forNum + forCount;
			int j = forCount;
			ImageIcon nextPage = new ImageIcon("./src/페이지_다음.png");
			JButton btnNextPage = new JButton(nextPage);
			btnNextPage.setSize(127, 50);
			btnNextPage.setBorderPainted(false);
			btnNextPage.setContentAreaFilled(false);
			btnNextPage.setFocusPainted(false);
			
			
			btnNextPage.setLocation(
					((int) getSize().getWidth() /2 + 30), 
					(int) getLocation().getY() / 2 + 550);
			
			add(btnNextPage);
			
			btnNextPage.addActionListener(new ActionListener() {
				
				@Override
				public void actionPerformed(ActionEvent e) {
					FrameBase.getDispose();
					FrameBase.getInstance(new FrameCategoryChioce(restaurantList, categoryName, mood, j, k));
				}
			});
		}
		
		if(forNum >= pageView) {
			makeBackbutton(restaurantList, categoryName, mood, forNum, count);
			
		}
		
		JButton btnEnd = new JButton("");
		JButton btnBack = new JButton("");
		JButton btnHome = new JButton("");
		
		btnEnd.setSize(50, 50);
		btnEnd.setBorderPainted(false);
		btnEnd.setContentAreaFilled(false);
		btnEnd.setFocusPainted(false);
		
		btnEnd.setLocation(
				((int) getSize().getWidth() /2 + 90),
				(int) getLocation().getY() / 2 + 630);
		
		
		btnBack.setSize(50, 50);
		btnBack.setBorderPainted(false);
		btnBack.setContentAreaFilled(false);
		btnBack.setFocusPainted(false);
		
		btnBack.setLocation(
				((int) getSize().getWidth() /2 -27), 
				(int) getLocation().getY() / 2 + 630);
		
		
		btnHome.setSize(50, 50);
		btnHome.setBorderPainted(false);
		btnHome.setContentAreaFilled(false);
		btnHome.setFocusPainted(false);
		
		btnHome.setLocation(
				((int) getSize().getWidth() /2 -138), 
				(int) getLocation().getY() / 2 + 630);
		
		
		add(btnEnd);
		add(btnBack);
		add(btnHome);
		
		btnEnd.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
				
			}
		});
		
		btnBack.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategory(restaurantList));
				
			}
		});
		
		btnHome.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameFrist());
				
			}
		});
		
	}
	public void RestaurantShortPrint(RestaurantList restaurantList, int i) {
		this.ShortPrintPlaceName = PLACE_NAME_BASIC + restaurantList.Info().get(i).getPlaceName();
		this.ShortPrintCategory = CATEGORY_NAME_BASIC + restaurantList.Info().get(i).getCategoryName() + " > " +
				restaurantList.Info().get(i).getCategoryDetail();
		this.ShortPrintPlaceBest = PLACE_BEST_BASIC + restaurantList.Info().get(i).getPlaceBest();
		
	}
	
	public void makeButton(RestaurantList restaurantList, int i, String categoryName, String mood) {
		RestaurantShortPrint(restaurantList, i);
		JButton restaurantChioce = new JButton("<HTML><body style='text align:left'>" + ShortPrintPlaceName + "<br>" + 
												ShortPrintCategory + "<br>" + 
												ShortPrintPlaceBest + "</body></HTML>");
		restaurantChioce.setBackground(new Color(255, 241, 202)); 
		restaurantChioce.setSize(360, 60);
		restaurantChioce.setFocusPainted(false);
		restaurantChioce.setLocation(
				((int) getSize().getWidth() /2 -180), 
				(int) getLocation().getY() / 2 + height);
		
		restaurantChioce.setHorizontalAlignment(SwingConstants.LEFT);
		add(restaurantChioce);
		height += 60;
		
		restaurantChioce.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameGetRestaurantInfo(restaurantList, i, categoryName, mood));
				
				
			}
		});
	}
	
	public void makeBackbutton(RestaurantList restaurantList, String categoryName, String mood, int forNum, int count) {
		int backforCount=0;
		int backPageCount=0;
	
		for(int i=forNum - count;i>=0;i--) {
			backforCount++;
			if(categoryName.equals("ALL")) {
				backPageCount++;

			}
			else if(restaurantList.Info().get(i).getCategoryName().equals(categoryName)) {
				backPageCount++;
			}
			
			if(backPageCount == 8)
				break;
		}
		int k = forNum - count;
		int j = backforCount;
		ImageIcon backPage = new ImageIcon("./src/페이지_이전.png");
		JButton btnBackPage = new JButton(backPage);
		btnBackPage.setSize(127, 50);
		btnBackPage.setBorderPainted(false);
		btnBackPage.setContentAreaFilled(false);
		
		btnBackPage.setLocation(
				((int) getSize().getWidth() /2 - 160), 
				(int) getLocation().getY() / 2 + 550);
		
		add(btnBackPage);
		
		btnBackPage.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameCategoryChioce(restaurantList, categoryName, mood, j, k));
				
			}
		});

}
}
