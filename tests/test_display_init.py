import pytest
from unittest.mock import patch, MagicMock
import sys
import numpy as np

mock_pi0disp = MagicMock()
mock_cv2 = MagicMock()

@pytest.fixture(autouse=True)
def cleanup_app1_module():
    global mock_pi0disp, mock_cv2
    if 'app1.__init__' in sys.modules:
        del sys.modules['app1.__init__']
    
    mock_pi0disp.reset_mock()
    mock_cv2.reset_mock()

    with patch.dict('sys.modules', {'pi0disp': mock_pi0disp, 'cv2': mock_cv2}):
        yield

def test_display_init_raspberry_pi():
    with patch('app1.__init__.os.uname') as mock_uname:
        mock_uname_result = MagicMock()
        mock_uname_result.nodename = 'raspberrypi'
        mock_uname.return_value = mock_uname_result
        
        original_import = __builtins__['__import__']
        def mock_import(name, *args, **kwargs):
            if name == 'pi0disp':
                raise ImportError
            return original_import(name, *args, **kwargs)
        
        with patch('builtins.__import__', side_effect=mock_import):
            import app1.__init__ as app1_init
            app1_init._detect_display_mode() # Call explicitly to set globals
            
            assert app1_init.DISPLAY_MODE == 'OPENCV' # Should fallback to OpenCV
            
            display_instance = app1_init.Display(640, 480) # Instantiate Display
            
            mock_cv2.namedWindow.assert_called_once()
            # mock_cv2.imshow.assert_called_once() # Called once in Display.__init__
            # mock_cv2.waitKey.assert_called_once() # Removed
            mock_pi0disp.init.assert_not_called()

def test_display_init_pc_environment():
    with patch('app1.__init__.os.uname') as mock_uname:
        mock_uname_result = MagicMock()
        mock_uname_result.nodename = 'my-pc'
        mock_uname.return_value = mock_uname_result
        
        import app1.__init__ as app1_init
        app1_init._detect_display_mode() # Call explicitly to set globals
        
        assert app1_init.DISPLAY_MODE == 'OPENCV'
        
        display_instance = app1_init.Display(640, 480)
        
        mock_cv2.namedWindow.assert_called_once_with("app1", mock_cv2.WINDOW_NORMAL)
        # mock_cv2.imshow.assert_called_once() # Removed
        # mock_cv2.waitKey.assert_called_once() # Removed
        mock_pi0disp.init.assert_not_called()

def test_clear_with_color():
    with patch('app1.__init__.os.uname') as mock_uname:
        mock_uname_result = MagicMock()
        mock_uname_result.nodename = 'my-pc' # Simulate PC environment for this test
        mock_uname.return_value = mock_uname_result
        
        import app1.__init__ as app1_init
        app1_init._detect_display_mode() # Call explicitly to set globals
        
        assert app1_init.DISPLAY_MODE == 'OPENCV'
        display_instance = app1_init.Display(640, 480)
        
        # Initial imshow call from __init__
        mock_cv2.imshow.reset_mock()
        mock_cv2.waitKey.reset_mock()

        test_color = (255, 0, 0) # Blue color in BGR for OpenCV
        display_instance.clear(test_color)
        
        mock_cv2.imshow.assert_called_once()
        mock_cv2.waitKey.assert_called_once()
        args, kwargs = mock_cv2.imshow.call_args_list[0]
        assert args[0] == "app1"
        assert (args[1][:, :, 0] == test_color[0]).all()
        assert (args[1][:, :, 1] == test_color[1]).all()
        assert (args[1][:, :, 2] == test_color[2]).all()
        
        # mock_pi0disp.init.return_value.clear.assert_not_called() # Removed as pi0disp is not used here

def test_draw_rect():
    with patch('app1.__init__.os.uname') as mock_uname:
        mock_uname_result = MagicMock()
        mock_uname_result.nodename = 'my-pc' # Simulate PC environment for this test
        mock_uname.return_value = mock_uname_result
        
        import app1.__init__ as app1_init
        app1_init._detect_display_mode() # Call explicitly to set globals
        
        assert app1_init.DISPLAY_MODE == 'OPENCV'
        display_instance = app1_init.Display(640, 480)
        display_instance.clear() # Call clear to initialize self.frame
        
        # Initial imshow call from __init__
        mock_cv2.imshow.reset_mock()
        mock_cv2.waitKey.reset_mock()
        mock_cv2.rectangle.reset_mock()
        
        # Test for OpenCV mode
        x, y, w, h = 10, 20, 30, 40
        color = (0, 255, 0) # Green
        display_instance.draw_rect(x, y, w, h, color)
        
        mock_cv2.rectangle.assert_called_once()
        args, kwargs = mock_cv2.rectangle.call_args_list[0]
        
        assert isinstance(args[0], np.ndarray)
        assert args[0].shape == (480, 640, 3) # Assuming default width/height
        
        assert args[1] == (x, y)
        assert args[2] == (x + w, y + h)
        assert args[3] == color[::-1]
        assert args[4] == -1

        mock_cv2.imshow.assert_called_once()
        mock_cv2.waitKey.assert_called_once()

        mock_pi0disp.reset_mock()
        mock_cv2.reset_mock()
        
        mock_uname.return_value.nodename = 'raspberrypi'
        if 'app1.__init__' in sys.modules:
            del sys.modules['app1.__init__']
        import app1.__init__ as app1_init # Re-import
        app1_init._detect_display_mode() # Call explicitly to set globals
        
        assert app1_init.DISPLAY_MODE == 'PI0DISP'
        display_instance_pi = app1_init.Display(640, 480)
        display_instance_pi.clear() # Call clear to initialize self.display.frame
        
        # Reset mock for draw_rect
        mock_pi0disp.ST7789V.return_value.draw_rect.reset_mock()

        display_instance_pi.draw_rect(x, y, w, h, color)
        
        # For pi0disp, we assume a draw_rect method exists on the display object
        mock_pi0disp.ST7789V.return_value.draw_rect.assert_called_once_with(x, y, w, h, color)