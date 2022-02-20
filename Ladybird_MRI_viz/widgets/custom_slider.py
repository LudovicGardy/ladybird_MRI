"""
Note: When the same key is repeated multiples times,
the last value overwrite previous values. Previous values are not removed
to keep a track of older parameters.
"""

def custom_slider():

    slider = """QSlider::groove:horizontal {
    border: 1px solid #bbb;
    background: white;
    height: 10px;
    height: 5px;
    border-radius: 4px;
    }




    QSlider::sub-page:horizontal {
    background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,
        stop: 0 #66e, stop: 1 #bbf);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #bbf, stop: 1 #55f);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #D2CCC4, stop: 1 #2F4353);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #0D324D, stop: 1 #7F5A83);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #04619F, stop: 1 #000000);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #2A5470, stop: 1 #4C4177);
    background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,
        stop: 0 #0CBABA, stop: 1 #380036);
    border: 1px solid #777;
    border: 1px solid #000000;
    height: 10px;
    border-radius: 4px;
    }




    QSlider::add-page:horizontal {
    background: #fff;
    border: 1px solid #777;
    height: 10px;
    border-radius: 4px;
    }

    QSlider::handle:horizontal {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #eee, stop:1 #ccc);
    border: 1px solid #777;
    width: 13px;
    margin-top: -2px;
    margin-bottom: -2px;
    border-radius: 4px;
    }

    QSlider::handle:horizontal:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #fff, stop:1 #ddd);
    border: 1px solid #444;
    border-radius: 4px;
    }

    QSlider::sub-page:horizontal:disabled {
    background: #bbb;
    border-color: #999;
    }

    QSlider::add-page:horizontal:disabled {
    background: #eee;
    border-color: #999;
    }

    QSlider::handle:horizontal:disabled {
    background: #eee;
    border: 1px solid #aaa;
    border-radius: 4px;
    }"""

    return slider