from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
# 자체 DB 를 새로 만들어서 가상 공간에서 테스트 한다

class TestView(TestCase): 
    def test_post(self):
       self.client -= Client()
# client = 컴퓨터 / 컴퓨터에서 테스트해서 날리면 -> goorm 에서 돌아간다
    def test_post_list(self) : # test_ test 할 항목    
    # 1.1 포스트 목록 페이지 가져오는지 확인
        response = self.client.get('/blog/')
    # /blog 해서 urls.py 가서 페이지 가져오는 행동이 잘 되고 있는지 확인하는 것
    # 1.2 정상적으로 페이지 로드되는지 확인
        self.assertEqual(response.status_code, 200)
    # response 의 상태코드가 200 과 같은가 ? -> 200 : 성공. 제대로 load 했다는 뜻
    # 1.3 포스트 목록 페이지의 <title> 태그 중 'Blog' 가 있는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
    # 현재 들어온 내용을 나눠서 html 로 바꿔서 저장해주라
        self.assertEqual(soup.title.text, 'Blog')
    # title 의 text 가 Blog 와 같은가 ?
        # 1.4 <Nav> Navbar 가 있는지 확인
        navbar = soup.nav
        # soup 에 nav 가 있나 ? 결과는 navbar 에 들어감
        # 1.5 Blog , AboutMe 라는 문구가 네비게이션 바에 있는가
        self.assertIn('Blog', navbar.text )
        # assertIn() : 안에 있니 ?
        # Blog 라는 글자가 navbar 안에 있니 ?
        self.assertIn('About Me', navbar.text)
        # About Me 라는 글자가 navbar 안에 있니 ?

        

        # 2.1 포스트가 하나도 없는가
        self.assertIn(Post.objects.count(), 0)
        # 2.2 main area에 '아직 게시물이 없습니다' 라는 문구가 나타난다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)
        
        # 3.1 포스트가 2개 있다면
        post_001 = Post.objects.create(
            title = '첫번째 포스트입니다.',
            content = 'Hello World. We are the world.',
        )
        
        post_002 = Post.objects.create(
            title = '두번째 포스트입니다.',
            content = '1등이 전부가 아니잖아.',
        )
        
        self.assertEqual(Post.object.count(), 2)
        
        # 3.2 포스트 목록 페이지를 새로고침했을때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        
        # 3.3 main area 에 포스트가 2개 존재한다.
        main_area = soup.find('div', id='main_area')
        self.assertIn(Post_001.title, main_area.text)
        self.assertIn(Post_002.title, main_area.text)
        
        # 3.4 '아직 게시물이 없습니다.'라는 문구는 더 이상 나타나지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)