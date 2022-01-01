package frame;

import static frame.Constant.CATEGORY_NAME_BASIC;
import static frame.Constant.PHONE_BASIC;
import static frame.Constant.PLACE_BEST_BASIC;
import static frame.Constant.PLACE_NAME_BASIC;
import static frame.Constant.PLACE_URL_BASIC;
import static frame.Constant.RANDOM;
import static frame.Constant.ROAD_ADDRESS_NAME_BASIC;

import java.awt.Color;
import java.awt.Desktop;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.Random;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;

import restaurantDB.RestaurantList;


public class FrameRandomChioce extends JPanel{
	
	private int ad;
	
	public FrameRandomChioce(RestaurantList restaurantList, String categoryName, String mood) {
		setBackground(new Color(255, 192, 203));
		setLayout(null);
		setSize(400, 700);
		

		if(categoryName.equals(RANDOM)) {
			while(true) {
				int i=new Random().nextInt(restaurantList.Info().size());
				ad=i;
				
				if(mood.equals("선택안함")) {
					makeRestaurantInfo(restaurantList, i);
					break;
				}
				
				else if(restaurantList.Info().get(i).getMood().equals(mood)) {
					makeRestaurantInfo(restaurantList, i);
					break;
				}
				else
					continue;
			}
			
			
		}
		else {
			while(true) {
				int i=new Random().nextInt(restaurantList.Info().size());
				ad=i;
				if((restaurantList.Info().get(i).getCategoryName().equals(categoryName)) &&
						mood.equals("선택안함")) {
					makeRestaurantInfo(restaurantList, i);
					break;
					
				}
				else if((restaurantList.Info().get(i).getCategoryName().equals(categoryName)) &&
						(restaurantList.Info().get(i).getMood().equals(mood))) {
					makeRestaurantInfo(restaurantList, i);
					break;
				}else
					continue;
				
			}
		}
		
		//예약버튼 생성
		ImageIcon imageReservation = new ImageIcon("./src/예약하기.png");
		JButton reservation =new JButton(imageReservation);
		//예약버튼 편집
		reservation.setSize(100,90);
		reservation.setBorderPainted(false);
		reservation.setContentAreaFilled(false);
		reservation.setFocusPainted(false);
		reservation.setLocation(150,515);
		add(reservation);
		
		ImageIcon imageRoadMap = new ImageIcon("./src/길찾기.png");
		JButton roadMap =new JButton(imageRoadMap);
		//예약버튼 편집
		roadMap.setSize(100,90);
		roadMap.setBorderPainted(false);
		roadMap.setContentAreaFilled(false);
		roadMap.setFocusPainted(false);
		roadMap.setLocation(40,515);
		add(roadMap);
		
		//다시뽑기 버튼
		ImageIcon imageReroll1 = new ImageIcon("./src/다시뽑기_1.png");
		ImageIcon imageReroll2 = new ImageIcon("./src/다시뽑기_2.png");
		JButton reroll1 = new JButton(imageReroll1);
		JButton reroll2 = new JButton(imageReroll2);
		
		reroll1.setSize(100, 40);
		reroll1.setBorderPainted(false);
		reroll1.setContentAreaFilled(false);
		reroll1.setFocusPainted(false);
		
		reroll1.setLocation(
				((int) getSize().getWidth() /2 + 70), 
				(int) getLocation().getY() / 2 + 570);
		add(reroll1);
		
		reroll2.setSize(100, 80);
		reroll2.setBorderPainted(false);
		reroll2.setContentAreaFilled(false);
		reroll2.setFocusPainted(false);
		
		reroll2.setLocation(
				((int) getSize().getWidth() /2 + 70), 
				(int) getLocation().getY() / 2 + 510);
		add(reroll2);
		
		//하단버튼
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
		
		reservation.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new ReservationRandom(restaurantList, categoryName, mood, ad));
			}
		});
		
		roadMap.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					Desktop.getDesktop().browse(new URI(restaurantList.Info().get(ad).getPlaceUrl()));
				} catch (IOException e1) {
					e1.printStackTrace();
				} catch (URISyntaxException e1) {
					e1.printStackTrace();
				}
				
			}
		});
		
		
		reroll1.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameRandomChioce(restaurantList, categoryName, mood));
				
			}
		});
		
		reroll2.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameRandomChioce(restaurantList, categoryName, mood));
				
			}
		});
		
		btnHome.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameFrist());
				
			}
		});
		
		btnBack.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameRandom(restaurantList));
				
			}
		});
		
		btnEnd.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
				
			}
		});
		
	}
	
	public FrameRandomChioce(RestaurantList restaurantList, String categoryName, String mood, int i) {
		setBackground(new Color(255, 192, 203));
		setLayout(null);
		setSize(400, 700);
		
		
		if(categoryName.equals(RANDOM)) {
			while(true) {
				ad=i;
				if(mood.equals("선택안함")) {
					makeRestaurantInfo(restaurantList, i);
					break;
				}
				
				else if(restaurantList.Info().get(i).getMood().equals(mood)) {
					makeRestaurantInfo(restaurantList, i);
					break;
				}
				else
					continue;
			}
			
			
		}
		else {
			while(true) {
				ad=i;
				if((restaurantList.Info().get(i).getCategoryName().equals(categoryName)) &&
						mood.equals("선택안함")) {
					makeRestaurantInfo(restaurantList, i);
					break;
					
				}
				else if((restaurantList.Info().get(i).getCategoryName().equals(categoryName)) &&
						(restaurantList.Info().get(i).getMood().equals(mood))) {
					makeRestaurantInfo(restaurantList, i);
					break;
				}else
					continue;
				
			}
		}
		
		//예약버튼 생성
		ImageIcon imageReservation = new ImageIcon("./src/예약하기.png");
		JButton reservation =new JButton(imageReservation);
		//예약버튼 편집
		reservation.setSize(100,90);
		reservation.setBorderPainted(false);
		reservation.setContentAreaFilled(false);
		reservation.setFocusPainted(false);
		reservation.setLocation(150,515);
		add(reservation);
		
		ImageIcon imageRoadMap = new ImageIcon("./src/길찾기.png");
		JButton roadMap =new JButton(imageRoadMap);
		//예약버튼 편집
		roadMap.setSize(100,90);
		roadMap.setBorderPainted(false);
		roadMap.setContentAreaFilled(false);
		roadMap.setFocusPainted(false);
		roadMap.setLocation(40,515);
		add(roadMap);
		
		//다시뽑기 버튼
		ImageIcon imageReroll1 = new ImageIcon("./src/다시뽑기_1.png");
		ImageIcon imageReroll2 = new ImageIcon("./src/다시뽑기_2.png");
		JButton reroll1 = new JButton(imageReroll1);
		JButton reroll2 = new JButton(imageReroll2);
		
		reroll1.setSize(100, 40);
		reroll1.setBorderPainted(false);
		reroll1.setContentAreaFilled(false);
		reroll1.setFocusPainted(false);
		
		reroll1.setLocation(
				((int) getSize().getWidth() /2 + 70), 
				(int) getLocation().getY() / 2 + 570);
		add(reroll1);
		
		reroll2.setSize(100, 80);
		reroll2.setBorderPainted(false);
		reroll2.setContentAreaFilled(false);
		reroll2.setFocusPainted(false);
		
		reroll2.setLocation(
				((int) getSize().getWidth() /2 + 70), 
				(int) getLocation().getY() / 2 + 510);
		add(reroll2);
		
		//하단버튼
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
		
		reservation.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new ReservationRandom(restaurantList, categoryName, mood, ad));
			}
		});
		
		roadMap.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				try {
					Desktop.getDesktop().browse(new URI(restaurantList.Info().get(i).getPlaceUrl()));
				} catch (IOException e1) {
					e1.printStackTrace();
				} catch (URISyntaxException e1) {
					e1.printStackTrace();
				}
				
			}
		});
		
		
		reroll1.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameRandomChioce(restaurantList, categoryName, mood));
				
			}
		});
		
		reroll2.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameRandomChioce(restaurantList, categoryName, mood));
				
			}
		});
		
		btnHome.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameFrist());
				
			}
		});
		
		btnBack.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				FrameBase.getDispose();
				FrameBase.getInstance(new FrameRandom(restaurantList));
				
			}
		});
		
		btnEnd.addActionListener(new ActionListener() {
			
			@Override
			public void actionPerformed(ActionEvent e) {
				System.exit(0);
				
			}
		});
		
	}
	
	public void makeRestaurantInfo(RestaurantList restaurantList, int i) {
		JLabel fImage=new JLabel(HtmlUtils.imgHtmlParser(restaurantList.Info().get(i).getImageUrl()));
        fImage.setSize(364,280);
        fImage.setLocation(18,70);
        add(fImage);
		
		JLabel story = new JLabel("<HTML><body>" + 
				PLACE_NAME_BASIC + restaurantList.Info().get(i).getPlaceName() + "<br>" + 
						CATEGORY_NAME_BASIC + restaurantList.Info().get(i).getCategoryName() + " > " +
								restaurantList.Info().get(i).getCategoryDetail() + "<br>" +
						ROAD_ADDRESS_NAME_BASIC + restaurantList.Info().get(i).getAddressName() + "<br>" + 
						PLACE_BEST_BASIC + restaurantList.Info().get(i).getPlaceBest() + "<br>" + 
						PHONE_BASIC + restaurantList.Info().get(i).getPhone() + "</body></HTML>");
		story.setSize(580, 185);
		story.setLocation(20, 350);
		story.setBackground(new Color(255, 255, 255));
		story.setFont(new Font("여기어때 잘난체", Font.BOLD, 20));
		add(story);
	}

}
