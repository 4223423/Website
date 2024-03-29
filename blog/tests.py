from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category, Tag, Comment


class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_aaaa = User.objects.create_user(username='aaaa', password='somepassword')
        self.user_bbbb = User.objects.create_user(username='bbbb', password='somepassword')

        self.user_bbbb.is_staff = True
        self.user_bbbb.save()
        
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.tag_pyhon_kor = Tag.objects.create(name='파이썬 공부', slug='파이썬-공부')
        self.tag_pyhon = Tag.objects.create(name='python', slug='python')
        self.tag_hello = Tag.objects.create(name='hello', slug='hello')
        
        self.post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_bbbb
        )
            
        self.post_001.tags.add(self.tag_hello)
        
        self.post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_aaaa
        )

        self.post_003 = Post.objects.create(
            title='세번째 포스트입니다.',
            content='category가 없을 수도 있죠',
            author=self.user_aaaa
        )
        self.post_003.tags.add(self.tag_pyhon_kor)
        self.post_003.tags.add(self.tag_pyhon)
        
        self.comment_001 = Comment.objects.create(
            post = self.post_001, 
            author = self.user_aaaa,
            content = '첫 번째 댓글입니다.',
            
            
        )
        
        
        

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)


        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

    
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(
            f'{self.category_programming.name} ({self.category_programming.post_set.count()})',
            categories_card.text
        )
        self.assertIn(
            f'{self.category_music.name} ({self.category_music.post_set.count()})',
            categories_card.text
        )
        self.assertIn(f'미분류 (1)', categories_card.text)

    def test_post_list(self):
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Blog')

        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')  # id가 post-1인 div를 찾아서, 그 안에
        self.assertIn(self.post_001.title, post_001_card.text)  # title이 있는지
        self.assertIn(self.post_001.category.name, post_001_card.text)  # category가 있는지
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)  # 작성자명이 있는지

        self.assertIn(self.tag_hello.name, post_001_card.text)
        self.assertNotIn(self.tag_pyhon.name, post_001_card.text)
        self.assertNotIn(self.tag_pyhon_kor.name, post_001_card.text)
        
        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)

        self.assertNotIn(self.tag_hello.name, post_002_card.text)
        self.assertNotIn(self.tag_pyhon.name, post_002_card.text)
        self.assertNotIn(self.tag_pyhon_kor.name, post_002_card.text)
        
        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)

        self.assertNotIn(self.tag_hello.name, post_003_card.text)
        self.assertIn(self.tag_pyhon.name, post_003_card.text)
        self.assertIn(self.tag_pyhon_kor.name, post_003_card.text)
        
        # Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그를 찾습니다.
        self.assertIn('아직 게시물이 없습니다', main_area.text)

    
    def test_post_detail(self):
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.user_bbbb.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)
        
        # comment area
        comments_area = soup.find('div', id='comment-area')
        comment_001_area = comments_area.find('div', id='comment-1')
        self.assertIn(self.comment_001.author.username, comment_001_area.text)
        self.assertIn(self.comment_001.content, comment_001_area.text)
    
    
    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
        
        
    def test_tag_page(self) :
        response = self.client.get(self.tag_hello.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.tag_hello.name, soup.h1.text)
        # 태그h1에 tag_hello가 있냐 
        
        main_area = soup.find('div', id='main-area')
        self.assertIn(self.tag_hello.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)
        
    def test_create_post(self) :
        # 로그인이 안된 상태
        response = self.client.get('/blog/create_post')
        self.assertNotEqual(response.status_code, 200)
        
        self.client.login(username="aaaa", password="somepassword")
        response = self.client.get('/blog/create_post')
        self.assertNotEqual(response.status_code, 200)
        
        # 로그인을 한다.
        self.client.login(username='bbbb', password='somepassword')
        
        response = self.client.get('/blog/create_post/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Create Post - Blog', soup.title.text)
        main_area = soup.find('div', id='main-area')
        self.assertIn('Create New Post', main_area.text)
        
        tag_str_input = main_area.find('input', id="id_tags_str")
        self.assertTrue(tag_str_input)
        
        
        self.client.post(
            '/blog/create_post/', 
            {
                'title' : 'Post Form 만들기', 
                'content' : 'Post Form 페이지를 만듭시다.',
                'tags_str' : 'new tag; 한글 태그, python',
            }
        )
                
        last_post = Post.objects.last()
        self.assertEqual(last_post.title, 'Post Form 만들기')
        self.assertEqual(last_post.author.username, 'bbbb')
        
        self.assertEqual(last_post.tags.count(), 3)
        self.assertTrue(Tag.objects.get(name='new tag'))
        self.assertTrue(Tag.objects.get(name='한글 태그'))
                

    def test_update_post(self) :
        update_post_url = f'/blog/update_post/{self.post_003.pk}/'
        
        # 로그인 안된 경우
        response = self.client.get(update_post_url)
        self.assertNotEqual(response.status_code, 200)
        
        # 로그인 했지만 작성자가 아닌 경우
        self.assertNotEqual(self.post_003.author, self.user_bbbb)
        self.client.login(
            username = self.user_bbbb.username, 
            password = "somepassword"
        )
        
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 403)
        # 403 = 권한 없음, db에 접근할려고 하나 아이디랑 패스워드가 없을 경우
        # 404 = 파일이 없음
        
        
        # 로그인 했는데 작성자인 경우 (bbbb)
        self.client.login(
            username = self.post_003.author.username,
            password = 'somepassword'
        )
    
        response = self.client.get(update_post_url)
        self.assertEqual(response.status_code, 200) # 제대로 작동
        soup = BeautifulSoup(response.content, 'html.parser')
        
        self.assertEqual('Edit Post - Blog', soup.title.text)
        main_area = soup.find('div', id="main-area")
        self.assertIn('Edit Post', main_area.text)
        
        # 이렇게 넣어준다 
        response = self.client.post(
            update_post_url,
            {
                'title' : '세 번째 포스트를 수정했습니다.',
                'content' : '안녕 세계? 우리는 하나!',
                'category' : self.category_music.pk
            },
            follow = True
        )
        
        # 이렇게 넣은거 테스트
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id="main-area")
        self.assertIn('세 번째 포스트를 수정했습니다.', main_area.text)
        self.assertIn('안녕 세계? 우리는 하나!', main_area.text)
        self.assertIn(self.category_music.name, main_area.text)
        

    def test_comment_form(self) :
        self.assetEqual(Comment.objects.count(), 1)
        self.assetEqual(self.post_001.comments_set.count(), 1)
        
        #로그인하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assetEqual(response.status_code, 200)
        
        soup = BeautifulSoup(response.comtent, 'html.parser')
        
        comment_area = soup.find('div', id='comment-area')
        self.assertIn('log in and leave a comment', comment_area.text)
        self.assertFalse(comment_area.find('form', id='comment-form'))
        
        # 로그인한 상태
        self.client.login(username='aaaa', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comment_area = soup.find('div', id="comment-area")
        self.assertNotIn('log in and leave a comment', comment_area.text)
             
        comment_form = comment_area.find('form', id='comment-form')
        self.assertTrue(comment.form.find('textarea', id="id_content"))
        
        response = self.client.post(
            self.post_001.get_absolute_url() + 'new_comment/',
            {
                'content' : 'aaaa의 댓글입니다.',
            },
            follow = True
        
        )
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post_001.comment_set.count(), 2)
        
        new_comment = Comment.objects.last()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertIn(new_comment.post.title, soup.title.text)
        
        comment_area = soup.find('div', id='comment-area')
        new_comment_div = comment_area.find('div', id=f'comment-{new_comment.pk}')
        self.assertIn('aaaa', new_comment_div.text)
        self.assertIn('aaaa의 댓글입니다.', new_comment_div.text)
        
        
        
    def test_comment_update(self):
        comment_by_trump = Comment.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = 'aaaa의 댓글입니다.'
        )
        
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area = soup.find('div',id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-1-update-btn'))
        self.assertFalse(comment_area.find('a',id='comment-2-update-btn'))
        
        
        self.client.login(username='obama', password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area = soup.find('div',id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-2-update-btn'))
        comment_001_update_btn = comment_area.find('a',id='comment-1-update-btn')
        self.assertIn('edit',comment_001_update_btn.text)
        self.assertEqual(comment_001_update_btn.attrs['href'],'/blog/update_comment/1/')
        
        
        response = self.client.get('/blog/update_comment/1/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        self.assertEqual('Edit Comment - Blog',soup.title.text)
        update_comment_form = soup.find('form',id='comment-form')
        content_textarea = update_comment_form.find('textarea', id='id_content')
        self.assertIn(self.comment_001.content,content_textarea.text)

        response = self.client.post(
            f'/blog/update_comment/{ self.comment_001.pk }/',
            {
                'content': "bbbb의 댓글을 수정합니다."
            },
            follow = True
        )
        
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        comment_001_div =soup.find('div',id='comment-1')
        self.assertIn("bbbb의 댓글을 수정합니다.",comment_001_div.text)
        self.assertIn("Update: ",comment_001_div.text)
        
        
    def test_delete_comment(self):
        comment_by_trump = Comment.objects.create(
            post = self.post_001,
            author = self.user_trump,
            content = 'aaaa의 댓글입니다.'
        )
        self.assertEqual(Comment.objects.count(),2)
        self.assertEqual(self.post_001.comment_set.count(),2)
        
        # 로그인하지 않은 상태
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area =soup.find('div',id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-1-delete-btn'))
        self.assertFalse(comment_area.find('a',id='comment-2-delete-btn'))
        
        # trump 로그인한 상태
        self.client.login(username='aaaa',password='somepassword')
        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        
        comment_area =soup.find('div',id='comment-area')
        self.assertFalse(comment_area.find('a',id='comment-1-delete-btn'))
        comment_002_delete_modal_btn = comment_area.find('a',id='comment-2-delete-modal-btn')
        self.assertIn('delete',comment_002_delete_modal_btn.text)
        self.assertEqual(comment_002_delete_modal_btn.attrs['data-target'],'#deleteCommentModal-2')
        
        delete_comment_modal_002 = soup.find('div',id='deleteCommentModal-2')
        self.assertIn('Are You Sure',delete_comment_modal_002.text)
        really_delete_btn_002 = delete_comment_modal_002.find('a')
        self.assertIn('Delete',really_delete_btn_002.text)
        self.assertEqual(really_delete_btn_002.attrs['href'],'/blog/delete_comment/2/')
        
        response = self.client.get('/blog/delete_comment/2/',follow=True)
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content,'html.parser')
        self.assertIn(self.post_001.title,soup.title.text)
        comment_area = soup.find('div',id='comment-area')
        self.assertNotIn('aaaa의 댓글입니다.',comment_area.text)

        
        self.assertEqual(Comment.objects.count(),1)
        self.assertEqual(self.post_001.comment_set.count(),1)